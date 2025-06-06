from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class ClassCreate(BaseModel):
    name: str = Field(..., min_length=2)
    instructor: str = Field(..., min_length=2)
    datetime: datetime
    available_slots: int = Field(..., ge=0)

class ClassOut(BaseModel):
    id: int
    name: str
    instructor: str
    datetime: datetime
    available_slots: int

    class Config:
        from_attributes = True

class BookingRequest(BaseModel):
    class_id: int = Field(..., gt=0)
    client_name: str = Field(..., min_length=2)
    client_email: EmailStr

class BookingOut(BaseModel):
    id: int
    class_id: int
    client_name: str
    client_email: str

    class Config:
        from_attributes = True
