from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class FitnessClass(Base):
    __tablename__ = "fitness_classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    instructor = Column(String, nullable=False)
    datetime = Column(DateTime, nullable=False)
    available_slots = Column(Integer, nullable=False, default=0)

    # Relationship to bookings
    bookings = relationship("Booking", back_populates="fitness_class", cascade="all, delete-orphan")

class Booking(Base):
    __tablename__ = "bookings"
    __table_args__ = (UniqueConstraint('class_id', 'client_email', name='_class_client_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("fitness_classes.id"), nullable=False, index=True)
    client_name = Column(String, nullable=False)
    client_email = Column(String, nullable=False, index=True)

    # Relationship back to fitness class
    fitness_class = relationship("FitnessClass", back_populates="bookings")
