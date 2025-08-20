from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Boolean, Float, Text
from sqlalchemy.orm import relationship
from .db import Base

class Parent(Base):
    __tablename__ = "parents"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, nullable=True)
    google_sub = Column(String, unique=True, index=True, nullable=True)

    children = relationship("Child", back_populates="parent")
    bookings = relationship("Booking", back_populates="parent")
    reviews = relationship("Review", back_populates="parent")


class Child(Base):
    __tablename__ = "children"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    birth_year = Column(Integer, nullable=False)
    experience = Column(String, nullable=False)

    parent = relationship("Parent", back_populates="children")
    booking_children = relationship("BookingChild", back_populates="child")


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    booked = Column(Boolean, default=False)

    bookings = relationship("Booking", back_populates="session")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    price = Column(Float, nullable=False)
    num_of_kids = Column(Integer, nullable=False)
    location = Column(String, nullable=False)
    description = Column(Text)
    paid = Column(Boolean, default=False)

    parent = relationship("Parent", back_populates="bookings")
    session = relationship("Session", back_populates="bookings")
    booking_children = relationship("BookingChild", back_populates="booking")


class BookingChild(Base):
    __tablename__ = "booking_children"

    booking_id = Column(Integer, ForeignKey("bookings.id"), primary_key=True)
    child_id = Column(Integer, ForeignKey("children.id"), primary_key=True)

    booking = relationship("Booking", back_populates="booking_children")
    child = relationship("Child", back_populates="booking_children")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    parent_id = Column(Integer, ForeignKey("parents.id"), nullable=False)
    date = Column(Date, nullable=False)
    rating = Column(Integer, nullable=False)
    description = Column(Text)

    parent = relationship("Parent", back_populates="reviews")
