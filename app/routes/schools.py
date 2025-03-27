from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import School
from app.schemas import SchoolResponse, SchoolCreate
from typing import List

router = APIRouter()

@router.get("/schools", response_model=List[SchoolResponse])
def get_schools(db: Session = Depends(get_db)):
    """Fetch all schools for the registration form"""
    return db.query(School).all()


@router.post("/schools", response_model=SchoolResponse)
def create_school(school_in: SchoolCreate, db: Session = Depends(get_db)):
    existing = db.query(School).filter(School.name == school_in.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="School with this name already exists")
    
    school = School(name=school_in.name)
    db.add(school)
    db.commit()
    db.refresh(school)
    return school