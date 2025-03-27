from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from . import crud
from app.database import get_db
from app.routes.auth import get_current_user
from typing import List
import uuid

router = APIRouter()


@router.post("/", response_model=schemas.GroupResponse)
def create_group(
    group_in: schemas.GroupCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can create groups")
    return crud.create_group(db=db, group=group_in, teacher_id=current_user.id)

@router.post("/{group_id}/students/", response_model=schemas.UserResponse)
def add_student_to_group(
    group_id: uuid.UUID,
    student_in: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    group = crud.get_group(db=db, group_id=group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    if group.teacher_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.add_student_to_group(db=db, group_id=group_id, student_data=student_in)



@router.get("/my-groups", response_model=List[schemas.GroupResponseWithStudents])
def get_my_groups(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    groups = crud.get_user_groups(db=db, user_id=current_user.id, user_role=current_user.role)
    return [
        {
            "id": group.id,
            "name": group.name,
            "teacher_id": group.teacher_id,
            "students": [
                {"id": student.student.id, "name": student.student.full_name, "email": student.student.email}
                for student in group.students
            ]
        }
        for group in groups
    ]
