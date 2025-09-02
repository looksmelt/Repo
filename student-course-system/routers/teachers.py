from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from bson import ObjectId
from database import teachers_collection, courses_collection, enrollments_collection, students_collection
from models import TeacherCreate, Teacher, LoginRequest, Token
from utils import hash_password, verify_password, create_access_token, get_current_teacher, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List

router = APIRouter(prefix="/teachers", tags=["teachers"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_teacher(teacher: TeacherCreate):
    # 检查用户名是否已存在
    if teachers_collection.find_one({"username": teacher.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # 检查教师编号是否已存在
    if teachers_collection.find_one({"teacher_id": teacher.teacher_id}):
        raise HTTPException(status_code=400, detail="Teacher ID already exists")
    
    teacher_dict = teacher.dict()
    teacher_dict["password"] = hash_password(teacher_dict["password"])
    teacher_dict["created_at"] = datetime.now()
    teacher_dict["updated_at"] = datetime.now()
    
    result = teachers_collection.insert_one(teacher_dict)
    return {"id": str(result.inserted_id), "message": "Teacher registered successfully"}

@router.post("/login", response_model=Token)
async def login_teacher(login: LoginRequest):
    teacher = teachers_collection.find_one({"username": login.username})
    
    if not teacher or not verify_password(login.password, teacher["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": teacher["username"], "user_type": "teacher"}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=Teacher)
async def get_teacher_me(current_teacher: dict = Depends(get_current_teacher)):
    current_teacher["id"] = str(current_teacher["_id"])
    return current_teacher

@router.get("/{teacher_id}", response_model=Teacher)
async def get_teacher(teacher_id: str):
    teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher["id"] = str(teacher["_id"])
    return teacher

@router.get("/me/courses")
async def get_teacher_courses(current_teacher: dict = Depends(get_current_teacher)):
    teacher_id = str(current_teacher["_id"])
    
    # 获取教师教授的课程
    courses = list(courses_collection.find({"teacher_id": teacher_id}))
    
    for course in courses:
        course["id"] = str(course["_id"])
    
    return courses

@router.get("/me/courses/{course_id}/students")
async def get_course_students(course_id: str, current_teacher: dict = Depends(get_current_teacher)):
    teacher_id = str(current_teacher["_id"])
    
    # 检查教师是否教授该课程
    course = courses_collection.find_one({"_id": ObjectId(course_id), "teacher_id": teacher_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not taught by you")
    
    # 获取选修该课程的学生
    enrollments = list(enrollments_collection.find({"course_id": course_id}))
    student_ids = [enrollment["student_id"] for enrollment in enrollments]
    
    students = list(students_collection.find({"_id": {"$in": [ObjectId(sid) for sid in student_ids]}}))
    
    for student in students:
        student["id"] = str(student["_id"])
        # 移除密码等敏感信息
        if "password" in student:
            del student["password"]
    
    return students

@router.post("/me/courses/{course_id}/students/{student_id}/grade")
async def grade_student(course_id: str, student_id: str, grade: float, 
                       current_teacher: dict = Depends(get_current_teacher)):
    teacher_id = str(current_teacher["_id"])
    
    # 检查教师是否教授该课程
    course = courses_collection.find_one({"_id": ObjectId(course_id), "teacher_id": teacher_id})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found or not taught by you")
    
    # 检查学生是否选修该课程
    enrollment = enrollments_collection.find_one({
        "course_id": course_id,
        "student_id": student_id
    })
    
    if not enrollment:
        raise HTTPException(status_code=404, detail="Student not enrolled in this course")
    
    # 更新成绩
    enrollments_collection.update_one(
        {"_id": enrollment["_id"]},
        {"$set": {"grade": grade}}
    )
    
    # 同时更新学生文档中的成绩
    students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {"$set": {f"current_grades.{course_id}": grade}}
    )
    
    return {"message": "Grade updated successfully"}