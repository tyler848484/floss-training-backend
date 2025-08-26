from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud, app.schemas as schemas
from app.db import get_db
from typing import List
from app.jwt import get_current_parent

router = APIRouter(prefix="/parents", tags=["Parents"])

@router.get("/me", response_model=schemas.Parent)
def read_parent(db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    parent_id = user.get("id")
    db_parent = crud.get_parent(db, int(parent_id))
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@router.put("/me", response_model=schemas.Parent)
def update_parent(parent_update: schemas.ParentUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    parent_id = user.get("id")
    db_parent = crud.update_parent(db, parent_id, parent_update.phone_number)
    for child in parent_update.children:
        crud.create_child(db, parent_id, child)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent

@router.put("/phone", response_model=schemas.Parent)
def update_parent_phone(parent_update: schemas.ParentUpdatePhone, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    parent_id = user.get("id")
    db_parent = crud.update_parent(db, parent_id, parent_update.phone_number)
    if not db_parent:
        raise HTTPException(status_code=404, detail="Parent not found")
    return db_parent