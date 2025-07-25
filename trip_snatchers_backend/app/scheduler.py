from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from . import crud, email_utils
from .database import SessionLocal
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

async def scrape_holiday_price(url: str) -> float:
    """
    Placeholder for actual scraping logic. This should be implemented
    based on the specific holiday provider's website structure.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                # This is a placeholder - actual implementation would need
                # specific selectors for the holiday provider's website
                price_element = soup.find('span', {'class': 'price'})
                if price_element:
                    price_text = price_element.text.strip()
                    # Extract numbers from string (e.g., "£499.99" -> 499.99)
                    price = float(re.findall(r'\d+\.?\d*', price_text)[0])
                    return price
    return None

async def check_single_holiday(db: Session, holiday_track):
    """Check a single holiday track for price changes"""
    try:
        current_price = await scrape_holiday_price(holiday_track.url)
        if current_price and current_price <= holiday_track.target_price:
            # Create snatched deal
            crud.create_snatched_deal(
                db=db,
                user_id=holiday_track.user_id,
                holiday_track=holiday_track,
                snatched_price=current_price
            )
            
            # Send email notification
            user = crud.get_user(db, holiday_track.user_id)
            if user:
                email_utils.send_price_alert(
                    user_email=user.email,
                    holiday_url=holiday_track.url,
                    target_price=holiday_track.target_price
                )
    except Exception as e:
        print(f"Error checking holiday {holiday_track.url}: {str(e)}")

def check_holiday_prices():
    """
    Main function to check all active holiday tracks
    """
    db = SessionLocal()
    try:
        active_tracks = crud.get_active_holiday_tracks(db)
        
        # Create event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run all checks concurrently
        tasks = [check_single_holiday(db, track) for track in active_tracks]
        loop.run_until_complete(asyncio.gather(*tasks))
        
        loop.close()
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=check_holiday_prices,
        trigger=IntervalTrigger(hours=6),
        id='check_holiday_prices',
        name='Check holiday prices every 6 hours',
        replace_existing=True
    )
    scheduler.start()
    return scheduler 