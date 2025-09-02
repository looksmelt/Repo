from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List
import bcrypt
import jwt
import os
from dotenv import load_dotenv
import uvicorn

from database import students_collection, teachers_collection, courses_collection, enrollments_collection
from models import (
    StudentCreate, Student, TeacherCreate, Teacher, CourseCreate, Course, 
    Enrollment, LoginRequest, Token
)
from data_generator import generate_all_data

load_dotenv()

app = FastAPI(
    title="Student Course System",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password, hashed_password):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data, expires_delta=None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_type = payload.get("user_type")
        if username is None or user_type is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return {"username": username, "user_type": user_type}
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)

def get_current_student(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if user["user_type"] != "student":
        raise HTTPException(status_code=403, detail="Not a student")
    return user

def get_current_teacher(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if user["user_type"] != "teacher":
        raise HTTPException(status_code=403, detail="Not a teacher")
    return user

@app.post("/students/register", status_code=status.HTTP_201_CREATED)
def register_student(student: StudentCreate):
    if students_collection.find_one({"username": student.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if students_collection.find_one({"student_id": student.student_id}):
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    student_dict = student.model_dump()
    student_dict["password"] = hash_password(student_dict["password"])
    student_dict["created_at"] = datetime.now()
    student_dict["updated_at"] = datetime.now()
    
    result = students_collection.insert_one(student_dict)
    return {"id": str(result.inserted_id), "message": "Student registered successfully"}

@app.post("/teachers/register", status_code=status.HTTP_201_CREATED)
def register_teacher(teacher: TeacherCreate):
    if teachers_collection.find_one({"username": teacher.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if teachers_collection.find_one({"teacher_id": teacher.teacher_id}):
        raise HTTPException(status_code=400, detail="Teacher ID already exists")
    
    teacher_dict = teacher.model_dump()
    teacher_dict["password"] = hash_password(teacher_dict["password"])
    teacher_dict["courses"] = []
    teacher_dict["created_at"] = datetime.now()
    teacher_dict["updated_at"] = datetime.now()
    
    result = teachers_collection.insert_one(teacher_dict)
    return {"id": str(result.inserted_id), "message": "Teacher registered successfully"}

@app.post("/login", response_model=Token)
def login(login_data: LoginRequest):
    user = students_collection.find_one({"username": login_data.username})
    user_type = "student"
    
    if not user:
        user = teachers_collection.find_one({"username": login_data.username})
        user_type = "teacher"
    
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "user_type": user_type}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, current_user: dict = Depends(get_current_teacher)):
    if courses_collection.find_one({"name": course.name}):
        raise HTTPException(status_code=400, detail="Course name already exists")
    
    course_dict = course.model_dump()
    course_dict["created_at"] = datetime.now()
    course_dict["updated_at"] = datetime.now()
    course_dict["teacher_id"] = None
    
    result = courses_collection.insert_one(course_dict)
    return {"id": str(result.inserted_id), "message": "Course created successfully"}

@app.get("/courses", response_model=List[Course])
def get_courses():
    courses = list(courses_collection.find())
    
    for course in courses:
        course["id"] = str(course["_id"])
    
    return courses

@app.put("/courses/{course_id}/assign/{teacher_id}")
def assign_teacher_to_course(course_id: str, teacher_id: str, current_user: dict = Depends(get_current_teacher)):#current_user:dict 未存取
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    courses_collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {"teacher_id": teacher_id, "updated_at": datetime.now()}}
    )
    
    teachers_collection.update_one(
        {"_id": ObjectId(teacher_id)},
        {"$addToSet": {"courses": course_id}, "$set": {"updated_at": datetime.now()}}
    )
    
    return {"message": "Teacher assigned to course successfully"}

@app.get("/students/me", response_model=Student)
def get_student_me(current_user: dict = Depends(get_current_student)):
    student = students_collection.find_one({"username": current_user["username"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student["id"] = str(student["_id"])
    if "password" in student:
        del student["password"]
    
    return student

@app.get("/teachers/me", response_model=Teacher)
def get_teacher_me(current_user: dict = Depends(get_current_teacher)):
    teacher = teachers_collection.find_one({"username": current_user["username"]})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher["id"] = str(teacher["_id"])
    if "password" in teacher:
        del teacher["password"]
    
    return teacher

@app.get("/students/me/courses")
def get_student_courses(current_user: dict = Depends(get_current_student)):
    student = students_collection.find_one({"username": current_user["username"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_id = str(student["_id"])
    
    enrollments = list(enrollments_collection.find({"student_id": student_id}))
    course_ids = [enrollment["course_id"] for enrollment in enrollments]
    
    courses = list(courses_collection.find({"_id": {"$in": [ObjectId(cid) for cid in course_ids]}}))
    
    for course in courses:
        course["id"] = str(course["_id"])
    
    return courses

@app.post("/students/me/enroll/{course_id}")
def enroll_course(course_id: str, current_user: dict = Depends(get_current_student)):
    student = students_collection.find_one({"username": current_user["username"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_id = str(student["_id"])
    
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if not course.get("teacher_id"):
        raise HTTPException(status_code=400, detail="Course has no assigned teacher")
    
    existing_enrollment = enrollments_collection.find_one({
        "student_id": student_id,
        "course_id": course_id
    })
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    enrollment_count = enrollments_collection.count_documents({"course_id": course_id})
    if enrollment_count >= course["capacity"]:
        raise HTTPException(status_code=400, detail="Course is full")
    
    enrollment = {
        "student_id": student_id,
        "course_id": course_id,
        "teacher_id": course["teacher_id"],
        "enrolled_at": datetime.now()
    }
    
    enrollments_collection.insert_one(enrollment)
    return {"message": "Enrolled successfully"}

@app.get("/teachers/me/courses")
def get_teacher_courses(current_user: dict = Depends(get_current_teacher)):
    teacher = teachers_collection.find_one({"username": current_user["username"]})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher_id = str(teacher["_id"])
    
    courses = list(courses_collection.find({"teacher_id": teacher_id}))
    
    for course in courses:
        course["id"] = str(course["_id"])
    
    return courses

@app.post("/generate-data")
def generate_data():
    """生成测试数据"""
    try:
        generate_all_data()
        return {"message": "Data generated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating data: {str(e)}")

@app.get("/")
def root():
    return {"message": "Student Course System API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
