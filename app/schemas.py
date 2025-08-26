from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import date, time

class ChildBase(BaseModel):
    first_name: str
    last_name: str
    birth_year: int
    experience: str

class ChildCreate(ChildBase):
    pass

class Child(ChildBase):
    id: int
    parent_id: int
    class Config:
        orm_mode = True


class ParentBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: Optional[str] = None
    google_sub: str

class ParentCreate(ParentBase):
    pass

class ParentUpdate(BaseModel):
    phone_number: str
    children: List[ChildCreate]

class ParentUpdatePhone(BaseModel):
    phone_number: str

class Parent(ParentBase):
    id: int
    class Config:
        orm_mode = True


class SessionBase(BaseModel):
    date: date
    start_time: time
    end_time: time
    booked: bool

class SessionCreate(SessionBase):
    pass

class Session(SessionBase):
    id: int
    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    price: float
    num_of_kids: int
    paid: Optional[bool] = False

class BookingCreate(BookingBase):
    session_id: int
    child_ids: List[int]
    description: Optional[str] = None
    location: str

class Booking(BookingBase):
    id: int
    parent_id: int
    session_id: int
    description: Optional[str] = None
    location: str
    class Config:
        orm_mode = True

class BookingUpdate(BookingBase):
    child_ids: List[int]
    description: Optional[str] = None
    location: str

class BookingSummary(BaseModel):
    id: int
    description: Optional[str] = None
    location: str
    date: str
    start_time: str
    end_time: str
    paid: bool
    price: float
    children: List[Child]


class BookingChild(BaseModel):
    booking_id: int
    child_id: int
    class Config:
        orm_mode = True



class ReviewBase(BaseModel):
    date: date
    rating: int
    description: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class Review(ReviewBase):
    id: int
    parent_id: int
    class Config:
        orm_mode = True

class ReviewUpdate(BaseModel):
    rating: int
    description: Optional[str] = None

class ReviewWithParent(BaseModel):
    id: int
    parent_id: int
    date: date
    rating: int
    description: Optional[str] = None
    first_name: Optional[str] = None
