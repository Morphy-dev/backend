from sqlalchemy.orm import Session
from app.models import Lesson
from app.models import Group
from app.schemas import LessonCreate
import uuid

def create_lesson(db: Session, group_id: uuid.UUID, lesson_data: LessonCreate):
    # Ensure the group exists
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        return None  # Group not found

    # Create the lesson
    db_lesson = Lesson(id=uuid.uuid4(), title=lesson_data.title, group_id=group_id)
    db.add(db_lesson)
    db.commit()
    db.refresh(db_lesson)
    return db_lesson

def get_lessons_by_group(db: Session, group_id: uuid.UUID):
    return db.query(Lesson).filter(Lesson.group_id == group_id).all()
