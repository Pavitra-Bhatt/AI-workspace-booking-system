from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any
from datetime import datetime

from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.models import User, Appointment
from backend.app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentUpdate
from backend.app.api.deps import get_current_user
from backend.app.services.email import send_appointment_confirmation

router = APIRouter()

@router.post("/api/appointments", response_model=AppointmentResponse)
def create_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_in: AppointmentCreate,
    current_user: User = Depends(get_current_user)
) -> Any:
    print(appointment_in, "ok")
    # Check for overlapping appointments
    overlapping = db.query(Appointment).filter(
        Appointment.start_time < appointment_in.end_time,
        Appointment.end_time > appointment_in.start_time,
        Appointment.status != "cancelled"
    ).first()
    
    if overlapping:
        raise HTTPException(
            status_code=400,
            detail="This time slot overlaps with an existing appointment"
        )
    
    appointment = Appointment(
        **appointment_in.dict(),
        user_id=current_user.id,
        status="pending"
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    # Send confirmation email
    send_appointment_confirmation(appointment)
    
    return appointment

@router.get("/api/appointments", response_model=List[AppointmentResponse])
def get_appointments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> Any:
    appointments = db.query(Appointment).filter(
        Appointment.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return appointments

@router.get("/api/appointments/{appointment_id}", response_model=AppointmentResponse)
def get_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    return appointment

@router.put("/api/appointments/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    appointment_in: AppointmentUpdate,
    current_user: User = Depends(get_current_user)
) -> Any:
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    
    for field, value in appointment_in.dict(exclude_unset=True).items():
        setattr(appointment, field, value)
    
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

@router.delete("/api/appointments/{appointment_id}", response_model=AppointmentResponse)
def delete_appointment(
    *,
    db: Session = Depends(get_db),
    appointment_id: int,
    current_user: User = Depends(get_current_user)
) -> Any:
    appointment = db.query(Appointment).filter(
        Appointment.id == appointment_id,
        Appointment.user_id == current_user.id
    ).first()
    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )
    
    appointment.status = "cancelled"
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment 