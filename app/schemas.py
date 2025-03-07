from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional
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
