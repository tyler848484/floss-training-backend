from sqlalchemy.orm import Session
import app.models as models, app.schemas as schemas
from typing import List, Optional
from datetime import date


# ---------- Parent CRUD ----------

def get_parent(db: Session, parent_id: int) -> Optional[models.Parent]:
    return db.query(models.Parent).filter(models.Parent.id == parent_id).first()

def get_parent_by_google_sub(db: Session, google_sub: str) -> Optional[models.Parent]:
    return db.query(models.Parent).filter(models.Parent.google_sub == google_sub).first()

def get_parent_by_email(db: Session, email: str) -> Optional[models.Parent]:
    return db.query(models.Parent).filter(models.Parent.email == email).first()

def create_parent(db: Session, parent: schemas.ParentCreate) -> models.Parent:
    db_parent = models.Parent(
        first_name=parent.first_name,
        last_name=parent.last_name,
        email=parent.email,
        phone_number=parent.phone_number,
        google_sub=parent.google_sub
    )
    db.add(db_parent)
    db.commit()
    db.refresh(db_parent)
    return db_parent

def update_parent(db: Session, parent_id: int, phone_number: str) -> Optional[models.Parent]:
    db_parent = get_parent(db, parent_id)
    if db_parent:
        db_parent.phone_number = phone_number
        db.commit()
        db.refresh(db_parent)
    return db_parent

# ---------- Child CRUD ----------

def get_child(db: Session, child_id: int) -> Optional[models.Child]:
    return db.query(models.Child).filter(models.Child.id == child_id).first()

def get_children_by_parent(db: Session, parent_id: int) -> List[models.Child]:
    return db.query(models.Child).filter(models.Child.parent_id == parent_id).all()

def create_child(db: Session, parent_id: int, child: schemas.ChildCreate) -> models.Child:
    db_child = models.Child(
        first_name=child.first_name,
        last_name=child.last_name,
        birth_year=child.birth_year,
        experience=child.experience,
        parent_id=parent_id
    )
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return db_child

def update_child(db: Session, child_id: int, child_update: schemas.ChildCreate) -> Optional[models.Child]:
    db_child = get_child(db, child_id)
    if db_child:
        db_child.first_name = child_update.first_name
        db_child.last_name = child_update.last_name
        db_child.birth_year = child_update.birth_year
        db_child.experience = child_update.experience
        db.commit()
        db.refresh(db_child)
    return db_child

def delete_child(db: Session, child_id: int) -> bool:
    db_child = get_child(db, child_id)
    if db_child:
        db.delete(db_child)
        db.commit()
        return True
    return False


# ---------- Session CRUD ----------

def get_available_sessions_by_date(db: Session, session_date: date):
    return db.query(models.Session).filter(
        models.Session.date == session_date,
        models.Session.booked == False
    ).all()


# ---------- Booking CRUD ----------

def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()

def get_bookings_by_parent(db: Session, parent_id: int) -> List[schemas.BookingSummary]:
    bookings = db.query(models.Booking).filter(models.Booking.parent_id == parent_id).all()
    result = []
    for booking in bookings:
        session = db.query(models.Session).filter(models.Session.id == booking.session_id).first()
        # Get children for this booking
        booking_children = db.query(models.BookingChild).filter(models.BookingChild.booking_id == booking.id).all()
        children = []
        for bc in booking_children:
            child = db.query(models.Child).filter(models.Child.id == bc.child_id).first()
            if child:
                children.append({
                    "id": child.id,
                    "first_name": child.first_name,
                    "last_name": child.last_name,
                    "birth_year": child.birth_year,
                    "experience": child.experience,
                    "parent_id": child.parent_id
                })
        booking_dict = {
            "id": booking.id,
            "description": booking.description,
            "location": booking.location,
            "date": session.date.isoformat() if session else None,
            "start_time": session.start_time.strftime('%H:%M') if session else None,
            "end_time": session.end_time.strftime('%H:%M') if session else None,
            "paid": booking.paid,
            "price": booking.price,
            "children": children
        }
        result.append(booking_dict)
    return result

def get_bookings_by_session(db: Session, session_id: int) -> List[models.Booking]:
    return db.query(models.Booking).filter(models.Booking.session_id == session_id).all()

def create_booking(db: Session, booking: schemas.BookingCreate, parent_id: int) -> models.Booking:
    db_booking = models.Booking(
        parent_id=parent_id,
        session_id=booking.session_id,
        price=booking.price,
        num_of_kids=booking.num_of_kids,
        paid=booking.paid,
        location=booking.location,
        description=booking.description
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)

    for child_id in booking.child_ids:
        booking_child = models.BookingChild(
            booking_id=db_booking.id,
            child_id=child_id
        )
        db.add(booking_child)
    db.commit()

    session = db.query(models.Session).filter(models.Session.id == booking.session_id).first()
    if session:
        session.booked = True
        db.commit()

    return db_booking

def update_booking(db: Session, booking_id: int, booking_update: schemas.BookingUpdate) -> Optional[models.Booking]:
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db_booking.price = booking_update.price
        db_booking.num_of_kids = booking_update.num_of_kids
        db_booking.description = booking_update.description
        db_booking.location = booking_update.location
        db.commit()
        db.refresh(db_booking)

        db.query(models.BookingChild).filter(models.BookingChild.booking_id == booking_id).delete()
        db.commit()
        for child_id in booking_update.child_ids:
            booking_child = models.BookingChild(
                booking_id=booking_id,
                child_id=child_id
            )
            db.add(booking_child)
        db.commit()

    return db_booking

def delete_booking(db: Session, booking_id: int) -> bool:
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db.query(models.BookingChild).filter(models.BookingChild.booking_id == booking_id).delete()
        db.commit()

        session = db.query(models.Session).filter(models.Session.id == db_booking.session_id).first()
        if session:
            session.booked = False
            db.commit()

        db.delete(db_booking)
        db.commit()
        return True
    return False


# ---------- BookingChild CRUD ----------

def get_booking_child(db: Session, booking_id: int, child_id: int) -> Optional[models.BookingChild]:
    return db.query(models.BookingChild).filter(
        models.BookingChild.booking_id == booking_id,
        models.BookingChild.child_id == child_id
    ).first()

def create_booking_child(db: Session, booking_id: int, child_id: int) -> models.BookingChild:
    db_bc = models.BookingChild(
        booking_id=booking_id,
        child_id=child_id
    )
    db.add(db_bc)
    db.commit()
    db.refresh(db_bc)
    return db_bc

def delete_booking_child(db: Session, booking_id: int, child_id: int) -> bool:
    db_bc = get_booking_child(db, booking_id, child_id)
    if db_bc:
        db.delete(db_bc)
        db.commit()
        return True
    return False


# ---------- Review CRUD ----------

def get_review(db: Session, review_id: int) -> Optional[models.Review]:
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def get_reviews_by_parent(db: Session, parent_id: int):
    return db.query(models.Review).filter(models.Review.parent_id == parent_id).all()

def get_reviews(db: Session, skip: int = 0, limit: int = 100):
    reviews = db.query(models.Review).offset(skip).limit(limit).all()
    result = []
    for review in reviews:
        parent = db.query(models.Parent).filter(models.Parent.id == review.parent_id).first()
        review_dict = {
            "id": review.id,
            "parent_id": review.parent_id,
            "date": review.date,
            "rating": review.rating,
            "description": review.description,
            "first_name": parent.first_name if parent else None
        }
        result.append(review_dict)
    return result

def create_review(db: Session, review: schemas.ReviewCreate, parent_id: int) -> models.Review:
    db_review = models.Review(
        parent_id=parent_id,
        date=review.date,
        rating=review.rating,
        description=review.description,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review

def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate) -> Optional[models.Review]:
    db_review = get_review(db, review_id)
    if db_review:
        db_review.rating = review_update.rating
        db_review.description = review_update.description
        db.commit()
        db.refresh(db_review)
    return db_review

def delete_review(db: Session, review_id: int) -> bool:
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False
