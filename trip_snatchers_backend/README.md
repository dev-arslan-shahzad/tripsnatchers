# Trip Snatchers Backend

A FastAPI backend service for tracking and snatching holiday deals.

## Features

- User authentication with JWT
- Holiday price tracking
- Automated price checking every 6 hours
- Email notifications when target prices are met
- Public and user-specific snatched deals history

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

4. Run the development server:
```bash
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at http://localhost:8000/docs
- ReDoc documentation at http://localhost:8000/redoc

## API Endpoints

### Authentication
- POST `/auth/register` - Register new user
- POST `/auth/login` - Get access token

### Users
- GET `/users/me` - Get current user profile
- PUT `/users/me` - Update profile
- DELETE `/users/me` - Delete account

### Holidays
- POST `/holidays/track` - Track a holiday
- GET `/holidays/my-trips` - Get user's tracked holidays
- GET `/holidays/{id}` - Get specific tracked holiday
- DELETE `/holidays/{id}` - Remove tracking

### Snatched Deals
- GET `/snatched/all` - List all public snatched deals
- GET `/snatched/my` - List user's snatched deals

## Development

The project structure follows standard FastAPI practices:

```
trip_snatchers_backend/
├── app/
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic models
│   ├── crud.py          # Database operations
│   ├── email_utils.py    # Email functionality
│   ├── scheduler.py      # Price check scheduler
│   └── routes/          # API endpoints
├── scraping_scripts/     # Future scraping implementations
└── requirements.txt      # Python dependencies
```

## Security Notes

1. In production:
   - Replace the hardcoded SECRET_KEY in auth.py with an environment variable
   - Configure specific CORS origins instead of "*"
   - Use proper SSL/TLS for SMTP
   - Implement rate limiting
   - Add request validation

2. Email Setup:
   - For Gmail, use App Passwords: https://myaccount.google.com/apppasswords
   - Enable 2FA on your Google account first

## License

MIT 