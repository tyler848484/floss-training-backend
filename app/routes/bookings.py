from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import app.crud as crud, app.schemas as schemas
from app.db import get_db
from typing import List
from app.jwt import get_current_parent

router = APIRouter(prefix="/bookings", tags=["Bookings"])

@router.post("/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    return crud.create_booking(db, booking, user["id"])

@router.get("/", response_model=List[schemas.BookingSummary])
def read_bookings(
    db: Session = Depends(get_db), 
    user: dict = Depends(get_current_parent)
):
    return crud.get_bookings_by_parent(db, parent_id=user["id"])

@router.put("/{booking_id}", response_model=schemas.Booking)
def update_booking(booking_id: int, booking_update: schemas.BookingUpdate, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    db_booking = crud.update_booking(db, booking_id, booking_update)
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_booking

@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_parent)):
    success = crud.delete_booking(db, booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
