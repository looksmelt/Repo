from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from bson import ObjectId
from database import students_collection, enrollments_collection, courses_collection
from models import StudentCreate, Student, Enrollment, LoginRequest, Token
from utils import hash_password, verify_password, create_access_token, get_current_student, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import List

router = APIRouter(prefix="/students", tags=["students"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_student(student: StudentCreate):
    # 检查用户名是否已存在
    if students_collection.find_one({"username": student.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # 检查学号是否已存在
    if students_collection.find_one({"student_id": student.student_id}):
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    student_dict = student.dict()
    student_dict["password"] = hash_password(student_dict["password"])
    student_dict["current_grades"] = {}
    student_dict["past_grades"] = {}
    student_dict["created_at"] = datetime.now()
    student_dict["updated_at"] = datetime.now()
    
    result = students_collection.insert_one(student_dict)
    return {"id": str(result.inserted_id), "message": "Student registered successfully"}

@router.post("/login", response_model=Token)
async def login_student(login: LoginRequest):
    student = students_collection.find_one({"username": login.username})
    
    if not student or not verify_password(login.password, student["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": student["username"], "user_type": "student"}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=Student)
async def get_student_me(current_student: dict = Depends(get_current_student)):
    current_student["id"] = str(current_student["_id"])
    return current_student

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: str):
    student = students_collection.find_one({"_id": ObjectId(student_id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student["_id"])
    return student

@router.get("/me/courses")
async def get_student_courses(current_student: dict = Depends(get_current_student)):
    # 获取学生已选课程
    enrollments = list(enrollments_collection.find({"student_id": str(current_student["_id"])}))
    course_ids = [enrollment["course_id"] for enrollment in enrollments]
    
    courses = list(courses_collection.find({"_id": {"$in": [ObjectId(cid) for cid in course_ids]}}))
    
    for course in courses:
        course["id"] = str(course["_id"])
        # 移除敏感信息
        if "password" in course:
            del course["password"]
    
    return courses

@router.post("/me/enroll/{course_id}")
async def enroll_course(course_id: str, current_student: dict = Depends(get_current_student)):
    student_id = str(current_student["_id"])
    
    # 检查课程是否存在
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # 检查是否已选过该课程
    existing_enrollment = enrollments_collection.find_one({
        "student_id": student_id,
        "course_id": course_id
    })
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # 检查课程容量
    enrollment_count = enrollments_collection.count_documents({"course_id": course_id})
    if enrollment_count >= course["capacity"]:
        raise HTTPException(status_code=400, detail="Course is full")
    
    # 检查课程是否适合该学生（专业必修课需要匹配院系和班级）
    if (course["course_type"] == "required" and 
        (course.get("department") != current_student["department"] or 
         course.get("class_name") != current_student["class_name"])):
        raise HTTPException(status_code=400, detail="This course is not available for your department/class")
    
    # 创建选课记录
    enrollment = {
        "student_id": student_id,
        "course_id": course_id,
        "enrolled_at": datetime.now(),
        "grade": None
    }
    
    enrollments_collection.insert_one(enrollment)
    return {"message": "Enrolled successfully"}

@router.delete("/me/drop/{course_id}")
async def drop_course(course_id: str, current_student: dict = Depends(get_current_student)):
    student_id = str(current_student["_id"])
    
    result = enrollments_collection.delete_one({
        "student_id": student_id,
        "course_id": course_id
    })
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    return {"message": "Course dropped successfully"}