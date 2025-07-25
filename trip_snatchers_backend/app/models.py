from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    country = Column(String)
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(String, unique=True, nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)

    holiday_tracks = relationship("HolidayTrack", back_populates="user")
    snatched_deals = relationship("SnatchedDeal", back_populates="user")

class HolidayTrack(Base):
    __tablename__ = "holiday_tracks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    url = Column(String)
    target_price = Column(Float)
    current_price = Column(Float, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="holiday_tracks")

class SnatchedDeal(Base):
    __tablename__ = "snatched_deals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    holiday_url = Column(String)
    initial_price = Column(Float)
    target_price = Column(Float)
    snatched_price = Column(Float)
    date_tracked = Column(DateTime)
    date_snatched = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="snatched_deals") 