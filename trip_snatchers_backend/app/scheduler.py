from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy.orm import Session
from . import crud, email_utils
from .database import SessionLocal
import logging
from scraping_scripts.scraper import update_all_tracked_holiday_prices

def check_holiday_prices():
    """
    Main function to check all active holiday tracks using Selenium-based scraper
    """
    logging.info("Running Selenium-based holiday price updater...")
    update_all_tracked_holiday_prices()


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