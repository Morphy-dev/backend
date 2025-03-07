from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import School
from app.schemas import SchoolResponse
from typing import List

router = APIRouter()

@router.get("/schools", response_model=List[SchoolResponse])
def get_schools(db: Session = Depends(get_db)):
    """Fetch all schools for the registration form"""
    return db.query(School).all()
