import logging
from datetime import datetime
from sqlalchemy.orm import Session
from app import models
from app.database import SessionLocal
from .test import FixedHolidayPriceScraper
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configure logging
logger = logging.getLogger('HolidayPriceUpdater')


def scrape_and_update_single_holiday(holiday_id: int):
    """
    Scrape and update the price for a single holiday by its ID.
    """
    db: Session = SessionLocal()
    scraper = FixedHolidayPriceScraper(headless=True)
    try:
        holiday = db.query(models.HolidayTrack).filter(models.HolidayTrack.id == holiday_id).first()
        if not holiday:
            logger.warning(f"Holiday with ID {holiday_id} not found.")
            return
        logger.info(f"Scraping price for new holiday: {holiday.url}")
        price_str, date_str = scraper._scrape_price_and_date(holiday.url)
        logger.info(f"Scraped price: {price_str}, date: {date_str}")
        numeric_price = None
        if price_str and isinstance(price_str, str):
            import re
            match = re.search(r'[\d,.]+', price_str.replace(',', ''))
            if match:
                try:
                    numeric_price = float(match.group().replace(',', ''))
                except Exception:
                    numeric_price = None
        if numeric_price:
            holiday.current_price = numeric_price
            holiday.updated_at = datetime.utcnow() if hasattr(holiday, 'updated_at') else holiday.created_at
            db.commit()
            logger.info(f"Updated DB: {holiday.url} -> {numeric_price}")

            # Snatching logic: if price is at or below target and holiday is still active
            if holiday.is_active and numeric_price <= holiday.target_price:
                from app.email_utils import send_price_alert
                from app.crud import create_snatched_deal
                user = db.query(models.User).filter(models.User.id == holiday.user_id).first()
                if user:
                    send_price_alert(
                        user_email=user.email,
                        holiday_url=holiday.url,
                        target_price=numeric_price
                    )
                    create_snatched_deal(
                        db=db,
                        user_id=user.id,
                        holiday_track=holiday,
                        snatched_price=numeric_price
                    )
        else:
            logger.warning(f"Could not extract numeric price for {holiday.url}: {price_str}")
    finally:
        scraper.close()
        db.close()


def update_all_tracked_holiday_prices():
    """
    Multi-threaded: Scrape and update current prices for all active tracked holidays in the database,
    using threads for each user and for each holiday of that user.
    """
    db: Session = SessionLocal()
    try:
        users = db.query(models.User).all()
        logger.info(f"Found {len(users)} users to update.")
        def update_user_holidays(user):
            user_db = SessionLocal()
            try:
                holidays = user_db.query(models.HolidayTrack).filter(models.HolidayTrack.user_id == user.id, models.HolidayTrack.is_active == True).all()
                logger.info(f"User {user.email}: {len(holidays)} holidays to update.")
                def update_holiday(holiday):
                    scraper = FixedHolidayPriceScraper(headless=True)
                    try:
                        logger.info(f"User {user.email}: Scraping {holiday.url}")
                        price_str = scraper._scrape_price(holiday.url)
                        logger.info(f"User {user.email}: Scraped price: {price_str}")
                        numeric_price = None
                        if price_str and isinstance(price_str, str):
                            import re
                            match = re.search(r'[\d,.]+', price_str.replace(',', ''))
                            if match:
                                try:
                                    numeric_price = float(match.group().replace(',', ''))
                                except Exception:
                                    numeric_price = None
                        if numeric_price:
                            holiday.current_price = numeric_price
                            holiday.updated_at = datetime.utcnow() if hasattr(holiday, 'updated_at') else holiday.created_at
                            user_db.commit()
                            logger.info(f"User {user.email}: Updated DB: {holiday.url} -> {numeric_price}")
                        else:
                            logger.warning(f"User {user.email}: Could not extract numeric price for {holiday.url}: {price_str}")
                    finally:
                        scraper.close()
                with ThreadPoolExecutor(max_workers=4) as holiday_executor:
                    holiday_futures = [holiday_executor.submit(update_holiday, h) for h in holidays]
                    for f in as_completed(holiday_futures):
                        pass  # Just wait for all to finish
            finally:
                user_db.close()
        with ThreadPoolExecutor(max_workers=4) as user_executor:
            user_futures = [user_executor.submit(update_user_holidays, u) for u in users]
            for f in as_completed(user_futures):
                pass  # Wait for all users to finish
        logger.info("Multi-threaded holiday price update complete.")
    finally:
        db.close() 