from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud, app.schemas as schemas
from app.db import get_db
from typing import List
from app.jwt import get_current_parent

router = APIRouter(prefix="/children", tags=["Children"])

from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, time

@router.post("/", response_model=schemas.Child)
def create_child(child: schemas.ChildCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    return crud.create_child(db, child)

@router.get("/", response_model=List[schemas.Child])
def read_children(db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    return crud.get_children_by_parent(db, parent_id=user["id"])

# @router.get("/{child_id}", response_model=schemas.Child)
# def read_child(child_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
#     db_child = crud.get_child(db, child_id)
#     if not db_child:
#         raise HTTPException(status_code=404, detail="Child not found")
#     return db_child

@router.put("/{child_id}", response_model=schemas.Child)
def update_child(child_id: int, child_update: schemas.ChildCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    db_child = crud.update_child(db, child_id, child_update)
    if not db_child:
        raise HTTPException(status_code=404, detail="Child not found")
    return db_child

@router.delete("/{child_id}", status_code=204)
def delete_child(child_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    success = crud.delete_child(db, child_id)
    if not success:
        raise HTTPException(status_code=404, detail="Child not found")
