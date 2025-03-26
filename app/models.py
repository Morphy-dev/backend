from sqlalchemy import Column, String, ForeignKey, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from passlib.context import CryptContext
import enum
import uuid
from .database import Base

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRole(enum.Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class School(Base):
    __tablename__ = "schools"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    name = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="school")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    cellphone = Column(String, unique=True, nullable=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"), nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False)  # ✅ Store UserRole as a string

    school = relationship("School", back_populates="users")

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self.password_hash)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    groups = relationship("Group", back_populates="teacher")
    student_groups = relationship("GroupStudent", back_populates="student")


class Group(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String, nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    teacher = relationship("User", back_populates="groups")
    students = relationship("GroupStudent", back_populates="group")
    lessons = relationship("Lesson", back_populates="group", cascade="all, delete-orphan")


class GroupStudent(Base):
    __tablename__ = "group_students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"))
    student_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))

    # Relationships
    group = relationship("Group", back_populates="students")
    student = relationship("User", back_populates="student_groups")

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String, nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"))

    # Relationship
    group = relationship("Group", back_populates="lessons")