from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud, app.schemas as schemas
from app.db import get_db
from typing import List
from app.jwt import get_current_parent
from datetime import date

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=schemas.Session)
def create_session(session: schemas.SessionCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    return crud.create_session(db, session)

@router.get("/{session_date}", response_model=List[schemas.Session])
def read_sessions(session_date: date, db: Session = Depends(get_db)):
    return crud.get_available_sessions_by_date(db, session_date)
