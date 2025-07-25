from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import auth, users, holidays, snatched
from .scheduler import start_scheduler

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Trip Snatchers API",
    description="API for tracking and snatching holiday deals",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://localhost:8080",  # Frontend development server
        "http://127.0.0.1:8080",
        "http://localhost:8000",  # Backend development server
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(holidays.router)
app.include_router(snatched.router)

# Start the scheduler
scheduler = start_scheduler()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Trip Snatchers API",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    } 