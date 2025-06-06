from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from database import get_db
from models import FitnessClass, Booking
from schemas import ClassOut, BookingRequest, BookingOut, ClassCreate
from seed import populate_classes
from utils import adjust_class_time
from logger import log_event

app = FastAPI(title="Fitness Studio Booking API")

@app.on_event("startup")
def initialize():
    populate_classes()
    log_event("Server started and classes seeded.")

@app.get("/classes", response_model=List[ClassOut])
def get_classes(tz: str = Query("Asia/Kolkata"), db: Session = Depends(get_db)):
    classes = db.query(FitnessClass).filter(FitnessClass.datetime >= datetime.utcnow()).all()
    return [adjust_class_time(c, tz) for c in classes]

@app.post("/book", response_model=BookingOut)
def book_class(payload: BookingRequest, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == payload.class_id).first()

    if not fitness_class:
        log_event("Booking failed: Class not found")
        raise HTTPException(status_code=404, detail="Class not found.")

    if fitness_class.available_slots <= 0:
        log_event("Booking failed: No available slots")
        raise HTTPException(status_code=400, detail="Class is fully booked.")

    fitness_class.available_slots -= 1
    db.add(fitness_class)

    new_booking = Booking(**payload.dict())
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    
    log_event(f"Booked: {payload.client_email} -> Class ID {payload.class_id}")
    return new_booking

@app.get("/bookings", response_model=List[BookingOut])
def fetch_bookings(email: str, db: Session = Depends(get_db)):
    bookings = db.query(Booking).filter(Booking.client_email == email).all()
    if not bookings:
        log_event(f"No bookings found for: {email}")
    return bookings

# Admin Endpoints (for dynamic class support)

@app.post("/admin/class", response_model=ClassOut)
def create_class(payload: ClassCreate, db: Session = Depends(get_db)):
    new_class = FitnessClass(**payload.dict())
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    log_event(f"Class created: {new_class.name}")
    return new_class

@app.put("/admin/class/{class_id}", response_model=ClassOut)
def update_class(class_id: int, payload: ClassCreate, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found.")

    for field, value in payload.dict().items():
        setattr(fitness_class, field, value)

    db.commit()
    db.refresh(fitness_class)
    log_event(f"Class updated: ID {class_id}")
    return fitness_class

@app.delete("/admin/class/{class_id}")
def delete_class(class_id: int, db: Session = Depends(get_db)):
    fitness_class = db.query(FitnessClass).filter(FitnessClass.id == class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Class not found.")
    
    db.delete(fitness_class)
    db.commit()
    log_event(f"Class deleted: ID {class_id}")
    return {"message": "Class deleted successfully."}
