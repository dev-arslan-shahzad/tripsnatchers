# from sqlalchemy import create_engine, text
# from database import SQLALCHEMY_DATABASE_URL

# def update_holiday_prices():
#     engine = create_engine(SQLALCHEMY_DATABASE_URL)
#     with engine.connect() as conn:
#         try:
#             conn.execute(text("""
#                 UPDATE holiday_tracks
#                 SET current_price = 1400
#                 WHERE id = 5
#             """))
#             conn.execute(text("""
#                 UPDATE holiday_tracks
#                 SET current_price = 1600
#                 WHERE id = 6
#             """))
#             conn.commit()
#             print("Prices updated successfully.")
#         except Exception as e:
#             print(f"Error updating holiday prices: {str(e)}")
#             raise

# if __name__ == "__main__":
#     update_holiday_prices()

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from app.email_utils import send_price_alert
from app.crud import create_snatched_deal
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')
logger = logging.getLogger("SnatchLogicOnly")

def run_snatch_logic():
    db: Session = SessionLocal()
    try:
        holidays = db.query(models.HolidayTrack).filter(models.HolidayTrack.is_active == True).all()
        logger.info(f"Found {len(holidays)} active holidays to check for snatching.")

        for holiday in holidays:
            if holiday.current_price is None:
                logger.info(f"Skipping {holiday.url} (no current price set).")
                continue

            if holiday.current_price <= holiday.target_price:
                user = db.query(models.User).filter(models.User.id == holiday.user_id).first()
                if user:
                    logger.info(f"Snatched: {holiday.url} at {holiday.current_price} for {user.email}")
                    send_price_alert(
                        user_email=user.email,
                        holiday_url=holiday.url,
                        target_price=holiday.current_price
                    )
                    create_snatched_deal(
                        db=db,
                        user_id=user.id,
                        holiday_track=holiday,
                        snatched_price=holiday.current_price
                    )
            else:
                logger.info(f"No snatch: {holiday.url} is {holiday.current_price} (target was {holiday.target_price})")

    finally:
        db.close()

if __name__ == "__main__":
    run_snatch_logic()
