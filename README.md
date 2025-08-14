# Floss Training Backend

This is the backend API for the Floss Training soccer booking system. It is built with FastAPI and uses PostgreSQL for data storage. The backend handles authentication (Google OAuth), parent/child/session/booking/review management, and JWT-based authorization.

## Features

- FastAPI REST API
- Google OAuth authentication
- JWT-based session management (via cookies)
- CRUD for parents, children, sessions, bookings, reviews
- PostgreSQL database

## Running Locally

### 1. Clone the repository

```bash
git clone https://github.com/tyler848484/floss-training-backend.git
cd floss-training-backend
```

### 2. Set up Python environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory with the following:

```
DATABASE_URL=postgresql://username:password@localhost:5432/floss_training
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/auth/callback
JWT_SECRET_KEY=your-jwt-secret-key
SESSION_SECRET_KEY=your-session-secret-key
```

### 4. Set up the database

- Make sure PostgreSQL is running locally.
- Create the database:

```bash
psql -U username
CREATE DATABASE floss_training;
```

- Run the table creation script:

```bash
python create_tables.py
```

### 5. Run the backend server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

## Database Setup

- Uses PostgreSQL
- Tables are created via `create_tables.py`
- Update `DATABASE_URL` in `.env` to match your local setup

## API Endpoints

- `/login` - Google OAuth login
- `/auth/callback` - OAuth callback
- `/logout` - Logout (clears JWT cookie)
- `/parents`, `/children`, `/sessions`, `/bookings`, `/reviews` - CRUD endpoints

## Notes

- All protected endpoints require a valid JWT cookie
- Frontend should use `credentials: 'include'` for API requests

---

For more details, see the code and comments in the repository.
