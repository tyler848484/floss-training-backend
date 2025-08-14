from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import parents, children, sessions, bookings, reviews, auth
from starlette.middleware.sessions import SessionMiddleware
import os

app = FastAPI(
    title="Private Soccer Training API",
    description="Backend API for private soccer training booking system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://your-production-site.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "your-very-secret-random-string"),
)

@app.get("/")
def root():
    return {"message": "Hello, Soccer Training API is running!"}

app.include_router(parents.router)
app.include_router(children.router)
app.include_router(sessions.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(auth.router)
