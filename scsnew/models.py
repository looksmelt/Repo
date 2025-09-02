from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class Gender(str, Enum):
    MALE = "男"
    FEMALE = "女"

class UserBase(BaseModel):
    username: str
    nickname: str
    signature: Optional[str] = None
    name: str
    gender: Gender
    age: int
    phone: str
    email: EmailStr
    address: str

class StudentCreate(BaseModel):
    username: str
    password: str
    nickname: str
    signature: Optional[str] = None
    name: str
    student_id: str
    department: str
    class_name: str
    gender: Gender
    age: int
    phone: str
    email: EmailStr
    address: str

class Student(UserBase):
    student_id: str
    department: str
    class_name: str
    current_grades: Dict[str, float] = {}
    past_grades: Dict[str, float] = {}
    
    class Config:
        from_attributes = True

class TeacherCreate(BaseModel):
    username: str
    password: str
    nickname: str
    signature: Optional[str] = None
    name: str
    teacher_id: str
    gender: Gender
    age: int
    phone: str
    email: EmailStr
    address: str

class Teacher(UserBase):
    teacher_id: str
    courses: List[str] = []
    
    class Config:
        from_attributes = True

class CourseType(str, Enum):
    PUBLIC_ELECTIVE = "公共选修课"
    PROFESSIONAL_REQUIRED = "专业必修课"

class CourseCreate(BaseModel):
    name: str
    description: Optional[str] = None
    course_type: CourseType
    department: Optional[str] = None  # 对于专业必修课，指定所属院系
    class_names: Optional[List[str]] = None  # 对于专业必修课，指定适用的班级

class Course(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    course_type: CourseType
    department: Optional[str] = None
    class_names: Optional[List[str]] = None
    teacher_id: Optional[str] = None
    
    class Config:
        from_attributes = True

class ScheduleCreate(BaseModel):
    course_id: str
    teacher_id: str
    classroom: str
    day_of_week: int = Field(..., ge=1, le=7)  # 1=Monday, 7=Sunday
    start_time: str  # Format: "HH:MM"
    end_time: str    # Format: "HH:MM"

class Schedule(BaseModel):
    id: str
    course_id: str
    teacher_id: str
    classroom: str
    day_of_week: int
    start_time: str
    end_time: str
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str