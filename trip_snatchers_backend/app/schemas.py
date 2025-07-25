from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    country: str
    age: Optional[int] = None
    gender: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None

class HolidayTrackBase(BaseModel):
    url: str
    target_price: float

class HolidayTrackCreate(HolidayTrackBase):
    current_price: Optional[float] = None

class HolidayTrack(HolidayTrackBase):
    id: int
    user_id: int
    current_price: Optional[float] = None
    is_active: bool = True
    created_at: datetime

    class Config:
        from_attributes = True

class SnatchedDealBase(BaseModel):
    holiday_url: str
    initial_price: float
    target_price: float
    snatched_price: float
    date_tracked: datetime
    date_snatched: datetime

class SnatchedDeal(SnatchedDealBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class UserStats(BaseModel):
    active_tracks: int
    total_savings: float

    class Config:
        from_attributes = True 