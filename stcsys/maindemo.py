from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from bson import ObjectId
from typing import List, Optional
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

# 加载环境变量
load_dotenv()

app = FastAPI(
    title="Student Course System",
    version="1.0.0"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 安全配置 - 提醒：在生产环境必须设置环境变量SECRET_KEY
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "your-secret-key-here"
    import warnings
    warnings.warn("使用默认密钥，生产环境中请设置SECRET_KEY环境变量", UserWarning)

ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def hash_password(password: str) -> str:
    """密码哈希处理"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """验证令牌并返回用户信息"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_type: str = payload.get("user_type")
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

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """获取当前登录用户"""
    return verify_token(token)

def get_current_student(current_user: dict = Depends(get_current_user)) -> dict:
    """获取当前登录学生（权限验证）"""
    if current_user["user_type"] != "student":
        raise HTTPException(status_code=403, detail="Not a student")
    return current_user

def get_current_teacher(current_user: dict = Depends(get_current_user)) -> dict:
    """获取当前登录教师（权限验证）"""
    if current_user["user_type"] != "teacher":
        raise HTTPException(status_code=403, detail="Not a teacher")
    return current_user

def validate_object_id(id_str: str) -> ObjectId:
    """验证ObjectId格式"""
    try:
        return ObjectId(id_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")

@app.post("/students/register", status_code=status.HTTP_201_CREATED)
def register_student(student: StudentCreate):
    """注册新学生"""
    if students_collection.find_one({"username": student.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if students_collection.find_one({"student_id": student.student_id}):
        raise HTTPException(status_code=400, detail="Student ID already exists")
    
    student_dict = student.model_dump()
    student_dict["password"] = hash_password(student_dict["password"])
    student_dict["created_at"] = datetime.utcnow()  # 使用UTC时间保持一致性
    student_dict["updated_at"] = datetime.utcnow()
    
    result = students_collection.insert_one(student_dict)
    return {"id": str(result.inserted_id), "message": "Student registered successfully"}

@app.post("/teachers/register", status_code=status.HTTP_201_CREATED)
def register_teacher(teacher: TeacherCreate):
    """注册新教师"""
    if teachers_collection.find_one({"username": teacher.username}):
        raise HTTPException(status_code=400, detail="Username already exists")
    
    if teachers_collection.find_one({"teacher_id": teacher.teacher_id}):
        raise HTTPException(status_code=400, detail="Teacher ID already exists")
    
    teacher_dict = teacher.model_dump()
    teacher_dict["password"] = hash_password(teacher_dict["password"])
    teacher_dict["courses"] = []  # 默认为空列表
    teacher_dict["created_at"] = datetime.utcnow()
    teacher_dict["updated_at"] = datetime.utcnow()
    
    result = teachers_collection.insert_one(teacher_dict)
    return {"id": str(result.inserted_id), "message": "Teacher registered successfully"}

@app.post("/login", response_model=Token)
def login(login_data: LoginRequest):
    """用户登录并获取令牌"""
    # 先检查是否为学生
    user = students_collection.find_one({"username": login_data.username})
    user_type = "student"
    
    # 不是学生则检查是否为教师
    if not user:
        user = teachers_collection.find_one({"username": login_data.username})
        user_type = "teacher"
    
    # 验证用户和密码
    if not user or not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 创建访问令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "user_type": user_type}, 
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/courses", status_code=status.HTTP_201_CREATED)
def create_course(course: CourseCreate, current_user: dict = Depends(get_current_teacher)):
    """创建新课程（教师权限）"""
    if courses_collection.find_one({"name": course.name}):
        raise HTTPException(status_code=400, detail="Course name already exists")
    
    course_dict = course.model_dump()
    course_dict["created_at"] = datetime.utcnow()
    course_dict["updated_at"] = datetime.utcnow()
    course_dict["teacher_id"] = None  # 默认未分配教师
    
    result = courses_collection.insert_one(course_dict)
    return {"id": str(result.inserted_id), "message": "Course created successfully"}

@app.get("/courses", response_model=List[Course])
def get_courses():
    """获取所有课程"""
    courses = list(courses_collection.find())
    
    # 处理返回数据格式
    for course in courses:
        course["id"] = str(course["_id"])
        del course["_id"]  # 删除原始ObjectId字段
    
    return courses

@app.put("/courses/{course_id}/assign/{teacher_id}")
def assign_teacher_to_course(
    course_id: str, 
    teacher_id: str, 
    current_user: dict = Depends(get_current_teacher)
):
    """为课程分配教师（教师权限）"""
    # 验证ID格式
    try:
        course_oid = ObjectId(course_id)
        teacher_oid = ObjectId(teacher_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid ID format")
    
    # 检查课程是否存在
    course = courses_collection.find_one({"_id": course_oid})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # 检查教师是否存在
    teacher = teachers_collection.find_one({"_id": teacher_oid})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # 更新课程信息
    courses_collection.update_one(
        {"_id": course_oid},
        {"$set": {"teacher_id": teacher_id, "updated_at": datetime.utcnow()}}
    )
    
    # 更新教师信息
    teachers_collection.update_one(
        {"_id": teacher_oid},
        {"$addToSet": {"courses": course_id}, "$set": {"updated_at": datetime.utcnow()}}
    )
    
    return {"message": "Teacher assigned to course successfully"}

@app.get("/students/me", response_model=Student)
def get_student_me(current_user: dict = Depends(get_current_student)):
    """获取当前学生信息"""
    student = students_collection.find_one({"username": current_user["username"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # 处理返回数据
    student["id"] = str(student["_id"])
    del student["_id"]
    student.pop("password", None)  # 确保不返回密码
    
    return student

@app.get("/teachers/me", response_model=Teacher)
def get_teacher_me(current_user: dict = Depends(get_current_teacher)):
    """获取当前教师信息"""
    teacher = teachers_collection.find_one({"username": current_user["username"]})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # 处理返回数据
    teacher["id"] = str(teacher["_id"])
    del teacher["_id"]
    teacher.pop("password", None)  # 确保不返回密码
    
    return teacher

@app.get("/students/me/courses")
def get_student_courses(current_user: dict = Depends(get_current_student)):
    """获取当前学生已注册的课程"""
    student = students_collection.find_one({"username": current_user["username"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_id = str(student["_id"])
    
    # 获取注册信息
    enrollments = list(enrollments_collection.find({"student_id": student_id}))
    course_ids = [enrollment["course_id"] for enrollment in enrollments]
    
    # 验证课程ID并获取课程信息
    try:
        object_ids = [ObjectId(cid) for cid in course_ids]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid course ID in enrollment")
    
    courses = list(courses_collection.find({"_id": {"$in": object_ids}}))
    
    # 处理返回数据
    for course in courses:
        course["id"] = str(course["_id"])
        del course["_id"]
    
    return courses

@app.post("/students/me/enroll/{course_id}")
def enroll_course(course_id: str, current_user: dict = Depends(get_current_student)):
    """学生注册课程"""
    # 验证课程ID
    try:
        course_oid = ObjectId(course_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid course ID format")
    
    # 获取学生信息
    student = students_collection.find_one({"username": current_user["username"]})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student_id = str(student["_id"])
    
    # 检查课程是否存在
    course = courses_collection.find_one({"_id": course_oid})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # 检查课程是否已分配教师
    if not course.get("teacher_id"):
        raise HTTPException(status_code=400, detail="Course has no assigned teacher")
    
    # 检查是否已注册
    existing_enrollment = enrollments_collection.find_one({
        "student_id": student_id,
        "course_id": course_id
    })
    
    if existing_enrollment:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    # 检查课程是否已满
    enrollment_count = enrollments_collection.count_documents({"course_id": course_id})
    if enrollment_count >= course.get("capacity", 0):
        raise HTTPException(status_code=400, detail="Course is full")
    
    # 创建注册记录
    enrollment = {
        "student_id": student_id,
        "course_id": course_id,
        "teacher_id": course["teacher_id"],
        "enrolled_at": datetime.utcnow()
    }
    
    enrollments_collection.insert_one(enrollment)
    return {"message": "Enrolled successfully"}

@app.get("/teachers/me/courses")
def get_teacher_courses(current_user: dict = Depends(get_current_teacher)):
    """获取当前教师教授的课程"""
    teacher = teachers_collection.find_one({"username": current_user["username"]})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    teacher_id = str(teacher["_id"])
    
    # 获取课程信息
    courses = list(courses_collection.find({"teacher_id": teacher_id}))
    
    # 处理返回数据
    for course in courses:
        course["id"] = str(course["_id"])
        del course["_id"]
    
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
    return {"message": "Student Course System API", "status": "running"}

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
