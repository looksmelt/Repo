from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum
import re

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    nickname: str = Field(..., min_length=1, max_length=50)
    signature: Optional[str] = Field(None, max_length=200)
    name: str = Field(..., min_length=1, max_length=100)
    gender: Gender
    age: int = Field(..., ge=1, le=150)
    phone: str
    email: EmailStr
    address: str = Field(..., max_length=200)

    @field_validator('phone')
    def validate_phone(cls, v):
        if not re.match(r'^1[3-9]\d{9}$', v):  # 简单的中国手机号验证
            raise ValueError('Invalid phone number format')
        return v

class StudentCreate(UserBase):
    password: str = Field(..., min_length=6)
    student_id: str = Field(..., min_length=1, max_length=20)
    department: str = Field(..., min_length=1, max_length=100)
    class_name: str = Field(..., min_length=1, max_length=50)

class Student(UserBase):
    id: str
    student_id: str
    department: str
    class_name: str
    current_grades: Dict[str, float] = {}
    past_grades: Dict[str, float] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class TeacherCreate(UserBase):
    password: str = Field(..., min_length=6)
    teacher_id: str = Field(..., min_length=1, max_length=20)
    courses: List[str] = []

class Teacher(UserBase):
    id: str
    teacher_id: str
    courses: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CourseType(str, Enum):
    PUBLIC_ELECTIVE = "public_elective"  # 公共选修课
    REQUIRED = "required"  # 专业必修课

class CourseCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    course_type: CourseType
    department: Optional[str] = Field(None, min_length=1, max_length=100)  # 对于公共选修课，此项为空
    class_name: Optional[str] = Field(None, min_length=1, max_length=50)  # 对于公共选修课，此项为空
    credits: float = Field(..., ge=0.5, le=10.0)
    capacity: int = Field(..., ge=1)

class Course(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    course_type: CourseType
    department: Optional[str] = None
    class_name: Optional[str] = None
    credits: float
    capacity: int
    teacher_id: Optional[str] = None
    schedule: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ClassSchedule(BaseModel):
    course_id: str
    teacher_id: str
    classroom: str = Field(..., min_length=1, max_length=50)
    day_of_week: int = Field(..., ge=1, le=7)  # 1-7 表示周一到周日
    start_time: str  # 格式: "HH:MM"
    end_time: str    # 格式: "HH:MM"

    @field_validator('start_time', 'end_time')
    def validate_time_format(cls, v):
        if not re.match(r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$', v):
            raise ValueError('Time must be in HH:MM format')
        return v

class Enrollment(BaseModel):
    student_id: str
    course_id: str
    enrolled_at: datetime
    grade: Optional[float] = Field(None, ge=0, le=100)

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    user_type: Optional[str] = None  # "student" or "teacher"