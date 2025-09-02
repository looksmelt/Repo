from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class StudentCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    nickname: str = Field(..., min_length=1, max_length=50)
    signature: Optional[str] = Field(None, max_length=200)
    name: str = Field(..., min_length=1, max_length=100)
    student_id: str = Field(..., min_length=1, max_length=20)
    gender: Gender
    age: int = Field(..., ge=1, le=150)
    phone: str
    email: EmailStr
    address: str = Field(..., max_length=200)

class Student(BaseModel):
    id: str
    username: str
    nickname: str
    signature: Optional[str]
    name: str
    student_id: str
    gender: Gender
    age: int
    phone: str
    email: EmailStr
    address: str
    created_at: datetime
    updated_at: datetime

class TeacherCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    name: str = Field(..., min_length=1, max_length=100)
    teacher_id: str = Field(..., min_length=1, max_length=20)
    gender: Gender
    age: int = Field(..., ge=1, le=150)
    phone: str
    email: EmailStr

class Teacher(BaseModel):
    id: str
    username: str
    name: str
    teacher_id: str
    gender: Gender
    age: int
    phone: str
    email: EmailStr
    courses: List[str]
    created_at: datetime
    updated_at: datetime

class CourseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    credits: float = Field(..., ge=0.5, le=10.0)
    capacity: int = Field(..., ge=1)

class Course(BaseModel):
    id: str
    name: str
    description: Optional[str]
    credits: float
    capacity: int
    teacher_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class Enrollment(BaseModel):
    student_id: str
    course_id: str
    teacher_id: str
    enrolled_at: datetime

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str