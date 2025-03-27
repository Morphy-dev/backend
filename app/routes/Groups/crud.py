from sqlalchemy.orm import Session
from app.models import Group
from app.models import GroupStudent
from app.models import User, UserProfile
from app.schemas import GroupCreate
from app.schemas import UserCreate
from sqlalchemy.orm import Session, joinedload
import uuid

def create_group(db: Session, group: GroupCreate, teacher_id: uuid.UUID):
    db_group = Group(id=uuid.uuid4(), name=group.name, teacher_id=teacher_id)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

def get_group(db: Session, group_id: uuid.UUID):
    return db.query(Group).filter(Group.id == group_id).first()

def add_student_to_group(db: Session, group_id: uuid.UUID, student_data: UserCreate):
     # 1. Create the user
    hashed_pw = User.hash_password(student_data.password)  # or however you hash it
    user = User(
        full_name=student_data.full_name,
        email=student_data.email,
        password_hash=hashed_pw,
        school_id=student_data.school_id,
        role="student",
    )
    db.add(user)
    db.flush()  # get the user.id now without commit

    # 2. Create the profile
    profile = UserProfile(
        user_id=user.id,
        picture_url=student_data.picture_url,
    )
    db.add(profile)

    # 3. Link to group
    link = GroupStudent(group_id=group_id, student_id=user.id)
    db.add(link)

    db.commit()
    db.refresh(user)
    return user

def get_user_groups(db: Session, user_id: uuid.UUID, user_role: str):
    if user_role == "teacher":
        return (
            db.query(Group)
            .filter(Group.teacher_id == user_id)
            .options(joinedload(Group.students).joinedload(GroupStudent.student))
            .all()
        )
    elif user_role == "student":
        return (
            db.query(Group)
            .join(GroupStudent)
            .filter(GroupStudent.student_id == user_id)
            .options(joinedload(Group.students).joinedload(GroupStudent.student))
            .all()
        )
    return []