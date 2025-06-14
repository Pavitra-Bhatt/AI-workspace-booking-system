# Appointment Booking System

A web application for managing appointments with calendar integration and email notifications.

## Features

- User authentication and authorization
- Calendar-based appointment scheduling
- Email notifications for appointments
- Admin dashboard for managing appointments
- Real-time availability checking
- Appointment status tracking

## Tech Stack

### Backend
- Python 3.8+
- FastAPI (Web Framework)
- SQLAlchemy (ORM)
- PostgreSQL (Database)
- Celery (Task Queue for Email Notifications)
- Redis (Message Broker)
- JWT (Authentication)

### Frontend
- React.js
- Material-UI
- FullCalendar.js
- Axios

## Project Structure

```
appointment-booking/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   └── deps.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py
│   │   │   └── session.py
│   │   ├── models/
│   │   ├── schemas/
│   │   └── services/
│   ├── celery_app.py
│   ├── requirements.txt
│   └── main.py
└── README.md
```

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the backend server:
```bash
uvicorn main:app --reload
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
npm start
```

## API Documentation

Once the server is running, visit `http://localhost:8000/docs` for the interactive API documentation.

## Environment Variables

Create a `.env` file with the following variables:

```
DATABASE_URL=postgresql://user:password@localhost:5432/appointment_db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License 