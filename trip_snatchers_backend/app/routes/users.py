from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/me", response_model=schemas.User)
async def read_current_user(
    current_user: models.User = Depends(get_current_user)
):
    """Get current user's profile"""
    return current_user

@router.patch("/me", response_model=schemas.User)
async def update_current_user(
    user_update: schemas.UserUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user's profile"""
    updated_user = crud.update_user(db, user_id=current_user.id, user=user_update)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.get("/me/stats", response_model=schemas.UserStats)
async def get_user_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's statistics"""
    # Get active holiday tracks
    active_tracks = len([h for h in current_user.holiday_tracks if h.is_active])
    
    # Calculate total savings from snatched deals
    total_savings = sum(
        deal.initial_price - deal.snatched_price 
        for deal in current_user.snatched_deals
    )
    
    return {
        "active_tracks": active_tracks,
        "total_savings": total_savings
    } 