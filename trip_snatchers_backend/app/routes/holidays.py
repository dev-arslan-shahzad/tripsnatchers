from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db
from .auth import get_current_user
from ..scheduler import scrape_holiday_price
import asyncio

router = APIRouter(
    prefix="/holidays",
    tags=["holidays"]
)

@router.post("/track", response_model=schemas.HolidayTrack)
async def track_holiday(
    holiday: schemas.HolidayTrackCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.create_holiday_track(
        db=db,
        holiday=holiday,
        user_id=current_user.id
    )

@router.post("/update-price/{holiday_id}", response_model=schemas.HolidayTrack)
async def update_holiday_price(
    holiday_id: int,
    current_price: float,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update the current price of a tracked holiday"""
    holiday = crud.get_holiday_track(db, holiday_id=holiday_id, user_id=current_user.id)
    if holiday is None:
        raise HTTPException(status_code=404, detail="Holiday not found")
    
    updated_holiday = crud.update_holiday_price(
        db=db,
        holiday_id=holiday_id,
        current_price=current_price
    )
    
    # Check if target price is met
    if current_price <= holiday.target_price:
        crud.create_snatched_deal(
            db=db,
            user_id=current_user.id,
            holiday_track=holiday,
            snatched_price=current_price
        )
    
    return updated_holiday

@router.get("/my-trips", response_model=List[schemas.HolidayTrack])
async def read_user_holidays(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    holidays = crud.get_user_holiday_tracks(
        db, user_id=current_user.id, skip=skip, limit=limit
    )
    return holidays

@router.get("/{holiday_id}", response_model=schemas.HolidayTrack)
async def read_holiday(
    holiday_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    holiday = crud.get_holiday_track(db, holiday_id=holiday_id, user_id=current_user.id)
    if holiday is None:
        raise HTTPException(status_code=404, detail="Holiday not found")
    return holiday

@router.delete("/{holiday_id}")
async def delete_holiday(
    holiday_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if crud.delete_holiday_track(db, holiday_id=holiday_id, user_id=current_user.id):
        return {"message": "Holiday tracking removed successfully"}
    raise HTTPException(status_code=404, detail="Holiday not found") 