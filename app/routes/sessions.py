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

# @router.get("/{session_id}", response_model=schemas.Session)
# def read_session(session_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
#     db_session = crud.get_session(db, session_id)
#     if not db_session:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return db_session

# @router.put("/{session_id}", response_model=schemas.Session)
# def update_session(session_id: int, session_update: schemas.SessionCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
#     db_session = crud.update_session(db, session_id, session_update)
#     if not db_session:
#         raise HTTPException(status_code=404, detail="Session not found")
#     return db_session

# @router.delete("/{session_id}", status_code=204)
# def delete_session(session_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
#     success = crud.delete_session(db, session_id)
#     if not success:
#         raise HTTPException(status_code=404, detail="Session not found")
