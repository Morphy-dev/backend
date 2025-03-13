from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.routes.auth import get_current_user
import uuid
from . import crud

from typing import List

router = APIRouter()

@router.post("/groups/{group_id}/lessons", response_model=schemas.LessonResponse)
def create_lesson(
    group_id: uuid.UUID,
    lesson_in: schemas.LessonCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Check if the group exists
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Ensure only the teacher who owns the group can add lessons
    if current_user.role != "teacher" or group.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add lessons")

    lesson = crud.create_lesson(db=db, group_id=group_id, lesson_data=lesson_in)
    return lesson

@router.get("/groups/{group_id}/lessons", response_model=List[schemas.LessonResponse])
def get_lessons(
    group_id: uuid.UUID,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Ensure the group exists
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    # Ensure only teachers or students in the group can view lessons
    if current_user.role == "teacher" and group.teacher_id == current_user.id:
        pass  # Allowed
    elif current_user.role == "student":
        student_in_group = db.query(models.GroupStudent).filter_by(group_id=group_id, student_id=current_user.id).first()
        if not student_in_group:
            raise HTTPException(status_code=403, detail="Not authorized to view lessons")
    else:
        raise HTTPException(status_code=403, detail="Not authorized to view lessons")

    return crud.get_lessons_by_group(db=db, group_id=group_id)
