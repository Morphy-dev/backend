from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional, List
from app.models import UserRole

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    cellphone: Optional[str]
    school_id: UUID
    password: str
    role: str  # ✅ Expect string instead of Enum

class UserResponse(BaseModel):
    id: UUID
    full_name: str
    email: EmailStr
    role: str  # ✅ Return string instead of Enum
    school_id: UUID

    class Config:
        from_attributes = True

class Token(BaseModel):  # ✅ Ensure this exists
    access_token: str
    token_type: str

class SchoolResponse(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: UUID
    teacher_id: UUID

    class Config:
        orm_mode = True


class StudentResponse(BaseModel):
    id: UUID
    name: str
    email: str

    class Config:
        orm_mode = True

class GroupResponseWithStudents(BaseModel):
    id: UUID
    name: str
    teacher_id: UUID
    students: List[StudentResponse]

    class Config:
        orm_mode = True


class LessonBase(BaseModel):
    title: str

class LessonCreate(LessonBase):
    pass

class LessonResponse(LessonBase):
    id: UUID
    group_id: UUID

    class Config:
        orm_mode = True