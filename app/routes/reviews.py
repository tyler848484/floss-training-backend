from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud, app.schemas as schemas
from app.db import get_db
from typing import List, Optional
from app.jwt import get_current_parent

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    return crud.create_review(db, review)

@router.get("/", response_model=List[schemas.Review])
def read_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    if parent_id is not None:
        return crud.get_reviews_by_parent(db, parent_id=parent_id)
    return crud.get_reviews(db, skip=skip, limit=limit)

@router.get("/{review_id}", response_model=schemas.Review)
def read_review(review_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    db_review = crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.put("/{review_id}", response_model=schemas.Review)
def update_review(review_id: int, review_update: schemas.ReviewCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    db_review = crud.update_review(db, review_id, review_update)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return db_review

@router.delete("/{review_id}", status_code=204)
def delete_review(review_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    success = crud.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="Review not found")
