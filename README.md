# TripSnatchers

TripSnatchers is a web application designed to help users find and track the best holiday deals. The application monitors holiday packages and notifies users when prices drop or when deals matching their preferences become available.

## Features

- 📱 Responsive design that works on desktop and mobile
- 🔐 Secure user authentication system
- ✉️ Email verification system
- 📊 Interactive dashboard for tracking holiday deals
- 🏖️ Holiday package tracking
- 📉 Price drop notifications
- 👥 User profile management
- 🔍 Compatible sites monitoring

## Tech Stack

### Frontend
- React + Vite
- TypeScript
- Tailwind CSS
- Shadcn/ui components
- React Hook Form
- React Router

### Backend
- FastAPI (Python)
- SQLAlchemy
- Alembic for database migrations
- SQLite database
- Background task scheduling

## Getting Started

### Prerequisites
- Node.js (v16 or higher)
- Python 3.12 or higher
- Git

### Frontend Setup
1. Clone the repository:
```bash
git clone https://github.com/dev-arslan-shahzad/tripsnatchers.git
cd tripsnatchers
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

### Backend Setup
1. Navigate to the backend directory:
```bash
cd trip_snatchers_backend
```

2. Create and activate a virtual environment:
```bash
python -m venv env
# On Windows
.\env\Scripts\activate
# On Unix or MacOS
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
tripsnatchers/
├── src/                    # Frontend source code
│   ├── api/               # API client functions
│   ├── components/        # React components
│   ├── context/          # React context providers
│   ├── hooks/            # Custom React hooks
│   ├── lib/              # Utility functions
│   └── pages/            # Page components
├── trip_snatchers_backend/  # Backend code
│   ├── app/              # Main application code
│   ├── alembic/          # Database migrations
│   └── scraping_scripts/ # Web scraping utilities
```

## Features in Detail

### User Authentication
- Secure signup and login system
- Email verification
- Password recovery

### Holiday Tracking
- Track multiple holiday packages
- Set price alerts
- View price history
- Receive notifications for price drops

### Dashboard
- Overview of tracked holidays
- Price trends and analytics
- Deal recommendations

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- Built with [Shadcn/ui](https://ui.shadcn.com/)
- Uses [FastAPI](https://fastapi.tiangolo.com/) for the backend
- Powered by [React](https://reactjs.org/) and [Vite](https://vitejs.dev/)
