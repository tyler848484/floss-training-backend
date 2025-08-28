from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import parents, children, sessions, bookings, reviews, auth
from starlette.middleware.sessions import SessionMiddleware
import os
from app.db import Base, engine

app = FastAPI(
    title="Floss Private Soccer Coaching API",
    description="Backend API for private soccer coaching booking system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://floss-private-soccer-coaching-ui.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY"),
)

@app.on_event("startup")
def create_tables_on_startup():
    Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Hello, Soccer Training API is running!"}

app.include_router(parents.router)
app.include_router(children.router)
app.include_router(sessions.router)
app.include_router(bookings.router)
app.include_router(reviews.router)
app.include_router(auth.router)
