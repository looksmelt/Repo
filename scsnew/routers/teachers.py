from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from database import db, TEACHERS_COLLECTION
from models import Teacher, TeacherCreate, LoginRequest
from typing import List

router = APIRouter(prefix="/teachers", tags=["teachers"])

def get_teachers_collection() -> Collection:
    return db[TEACHERS_COLLECTION]

@router.post("/", response_model=Teacher)
async def create_teacher(teacher: TeacherCreate, collection: Collection = Depends(get_teachers_collection)):
    # 检查用户名是否已存在
    if collection.find_one({"username": teacher.username}):
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    # 检查教师编号是否已存在
    if collection.find_one({"teacher_id": teacher.teacher_id}):
        raise HTTPException(status_code=400, detail="教师编号已存在")
    
    # 插入新教师
    teacher_dict = teacher.model_dump()
    result = collection.insert_one(teacher_dict)
    
    # 返回创建的教师
    created_teacher = collection.find_one({"_id": result.inserted_id})
    created_teacher["id"] = str(created_teacher["_id"])
    return created_teacher

@router.get("/", response_model=List[Teacher])
async def get_teachers(skip: int = 0, limit: int = 100, collection: Collection = Depends(get_teachers_collection)):
    teachers = list(collection.find().skip(skip).limit(limit))
    for teacher in teachers:
        teacher["id"] = str(teacher["_id"])
    return teachers

@router.get("/{teacher_id}", response_model=Teacher)
async def get_teacher(teacher_id: str, collection: Collection = Depends(get_teachers_collection)):
    teacher = collection.find_one({"teacher_id": teacher_id})
    if not teacher:
        raise HTTPException(status_code=404, detail="教师不存在")
    teacher["id"] = str(teacher["_id"])
    return teacher

@router.post("/login")
async def teacher_login(login_request: LoginRequest, collection: Collection = Depends(get_teachers_collection)):
    teacher = collection.find_one({
        "username": login_request.username,
        "password": login_request.password
    })
    
    if not teacher:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    teacher["id"] = str(teacher["_id"])
    return {"message": "登录成功", "teacher": teacher}