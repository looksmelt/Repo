from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from database import db, STUDENTS_COLLECTION
from models import Student, StudentCreate, LoginRequest
from typing import List

router = APIRouter(prefix="/students", tags=["students"])

def get_students_collection() -> Collection:
    return db[STUDENTS_COLLECTION]

@router.post("/", response_model=Student)
async def create_student(student: StudentCreate, collection: Collection = Depends(get_students_collection)):
    # 检查用户名是否已存在
    if collection.find_one({"username": student.username}):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查学号是否已存在
    if collection.find_one({"student_id": student.student_id}):
        raise HTTPException(status_code=400, detail="学号已存在")
    
    # 插入新学生
    student_dict = student.model_dump()
    result = collection.insert_one(student_dict)
    
    # 返回创建的学生
    created_student = collection.find_one({"_id": result.inserted_id})
    created_student["id"] = str(created_student["_id"])
    return created_student

@router.get("/", response_model=List[Student])
async def get_students(skip: int = 0, limit: int = 100, collection: Collection = Depends(get_students_collection)):
    students = list(collection.find().skip(skip).limit(limit))
    for student in students:
        student["id"] = str(student["_id"])
    return students

@router.get("/{student_id}", response_model=Student)
async def get_student(student_id: str, collection: Collection = Depends(get_students_collection)):
    student = collection.find_one({"student_id": student_id})
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    student["id"] = str(student["_id"])
    return student

@router.post("/login")
async def student_login(login_request: LoginRequest, collection: Collection = Depends(get_students_collection)):
    student = collection.find_one({
        "username": login_request.username,
        "password": login_request.password
    })
    
    if not student:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    student["id"] = str(student["_id"])
    return {"message": "登录成功", "student": student}