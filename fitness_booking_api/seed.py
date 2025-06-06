from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import FitnessClass
from database import SessionLocal
import pytz

def populate_classes() -> None:
    db: Session = SessionLocal()
    try:
        # Check if any classes exist already
        if db.query(FitnessClass).first():
            return

        # Get current time in IST and convert to UTC
        ist = pytz.timezone("Asia/Kolkata")
        now_ist = datetime.now(ist)
        now_utc = now_ist.astimezone(pytz.utc)

        classes = [
            FitnessClass(name="Yoga", instructor="Anand", datetime=now_utc + timedelta(hours=2), available_slots=5),
            FitnessClass(name="Zumba", instructor="Rajesh", datetime=now_utc + timedelta(days=1), available_slots=8),
            FitnessClass(name="HIIT", instructor="Sharat", datetime=now_utc + timedelta(days=2), available_slots=10),
        ]

        db.add_all(classes)
        db.commit()
    finally:
        db.close()
