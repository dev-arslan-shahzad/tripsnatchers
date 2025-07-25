from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional

from .. import crud, models, schemas
from ..database import get_db
from ..email_utils import send_verification_email, generate_verification_token

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    
    # Check if user is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified. Please check your email for verification link."
        )
    
    return user

@router.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        if not db_user.is_verified:
            # If user exists but not verified, generate new token and send email
            token, expires = generate_verification_token()
            crud.update_verification_token(db, db_user.id, token, expires)
            if send_verification_email(user.email, token):
                raise HTTPException(
                    status_code=status.HTTP_202_ACCEPTED,
                    detail="Account exists but not verified. New verification email sent."
                )
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Generate verification token
    token, expires = generate_verification_token()
    
    # Create user with verification token
    hashed_password = get_password_hash(user.password)
    db_user = crud.create_user(
        db=db,
        user=user,
        hashed_password=hashed_password,
        verification_token=token,
        verification_token_expires=expires
    )
    
    # Send verification email
    if not send_verification_email(user.email, token):
        # If email fails, still create the user but log the error
        print(f"Failed to send verification email to {user.email}")
    
    raise HTTPException(
        status_code=status.HTTP_201_CREATED,
        detail="Registration successful. Please check your email for verification link."
    )

@router.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is verified
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Email not verified",
                "user_id": user.id,
                "email": user.email
            }
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/resend-verification")
async def resend_verification_email(
    email: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    """Resend verification email"""
    print(f"Resending verification email to: {email}")  # Debug log
    
    user = crud.get_user_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    
    if user.is_verified:
        raise HTTPException(
            status_code=400,
            detail="Email already verified"
        )
    
    # Generate new verification token
    token, expires = generate_verification_token()
    crud.update_verification_token(db, user.id, token, expires)
    
    # Send new verification email
    if send_verification_email(user.email, token):
        return {"message": "Verification email sent successfully"}
    else:
        raise HTTPException(
            status_code=500,
            detail="Failed to send verification email"
        )

@router.get("/verify-email/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    """Verify user's email address"""
    user = crud.get_user_by_verification_token(db, token)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid verification token"
        )
    
    # Check if token is expired
    if user.verification_token_expires < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Verification token has expired"
        )
    
    # Mark user as verified and clear token
    crud.verify_user(db, user.id)
    
    return {"message": "Email verified successfully"} 