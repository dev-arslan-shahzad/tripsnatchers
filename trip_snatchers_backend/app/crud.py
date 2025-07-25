from sqlalchemy.orm import Session
from sqlalchemy import and_
from . import models, schemas
from datetime import datetime
from typing import List, Optional

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(
    db: Session,
    user: schemas.UserCreate,
    hashed_password: str,
    verification_token: str,
    verification_token_expires: datetime
):
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        phone=user.phone,
        country=user.country,
        age=user.age,
        gender=user.gender,
        hashed_password=hashed_password,
        verification_token=verification_token,
        verification_token_expires=verification_token_expires,
        is_verified=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_verification_token(db: Session, token: str):
    return db.query(models.User).filter(models.User.verification_token == token).first()

def verify_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.is_verified = True
        db_user.verification_token = None
        db_user.verification_token_expires = None
        db.commit()
        db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_verification_token(db: Session, user_id: int, token: str, expires: datetime):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.verification_token = token
        db_user.verification_token_expires = expires
        db.commit()
        db.refresh(db_user)
    return db_user

def create_holiday_track(
    db: Session, holiday: schemas.HolidayTrackCreate, user_id: int, current_price: Optional[float] = None
):
    holiday_data = holiday.model_dump()
    if current_price is not None:
        holiday_data['current_price'] = current_price
    
    db_holiday = models.HolidayTrack(
        **holiday_data,
        user_id=user_id
    )
    db.add(db_holiday)
    db.commit()
    db.refresh(db_holiday)
    return db_holiday

def get_user_holiday_tracks(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.HolidayTrack)\
        .filter(models.HolidayTrack.user_id == user_id)\
        .offset(skip).limit(limit).all()

def get_holiday_track(db: Session, holiday_id: int, user_id: int):
    return db.query(models.HolidayTrack)\
        .filter(
            and_(
                models.HolidayTrack.id == holiday_id,
                models.HolidayTrack.user_id == user_id
            )
        ).first()

def delete_holiday_track(db: Session, holiday_id: int, user_id: int):
    db_holiday = get_holiday_track(db, holiday_id, user_id)
    if db_holiday:
        db.delete(db_holiday)
        db.commit()
        return True
    return False

def create_snatched_deal(
    db: Session,
    user_id: int,
    holiday_track: models.HolidayTrack,
    snatched_price: float
):
    db_snatched = models.SnatchedDeal(
        user_id=user_id,
        holiday_url=holiday_track.url,
        initial_price=holiday_track.current_price,
        target_price=holiday_track.target_price,
        snatched_price=snatched_price,
        date_tracked=holiday_track.created_at,
        date_snatched=datetime.utcnow()
    )
    db.add(db_snatched)
    
    # Deactivate the holiday track
    holiday_track.is_active = False
    
    db.commit()
    db.refresh(db_snatched)
    return db_snatched

def get_user_snatched_deals(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.SnatchedDeal)\
        .filter(models.SnatchedDeal.user_id == user_id)\
        .offset(skip).limit(limit).all()

def get_all_snatched_deals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SnatchedDeal)\
        .offset(skip).limit(limit).all()

def get_active_holiday_tracks(db: Session):
    return db.query(models.HolidayTrack)\
        .filter(models.HolidayTrack.is_active == True).all() 