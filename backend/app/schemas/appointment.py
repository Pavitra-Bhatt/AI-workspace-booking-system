from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class AppointmentUpdate(AppointmentBase):
    status: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    id: int
    status: str
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True 