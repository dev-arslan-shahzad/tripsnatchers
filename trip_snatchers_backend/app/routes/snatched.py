from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db
from .auth import get_current_user

router = APIRouter(
    prefix="/snatched",
    tags=["snatched"]
)

@router.get("/all", response_model=List[schemas.SnatchedDeal])
async def read_all_snatched_deals(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all snatched deals across all users
    """
    return crud.get_all_snatched_deals(db, skip=skip, limit=limit)

@router.get("/my", response_model=List[schemas.SnatchedDeal])
async def read_user_snatched_deals(
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get all snatched deals for the current user
    """
    return crud.get_user_snatched_deals(
        db, user_id=current_user.id, skip=skip, limit=limit
    ) 