from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from database import db, COURSES_COLLECTION
from models import Course, CourseCreate
from typing import List

router = APIRouter(prefix="/courses", tags=["courses"])

def get_courses_collection() -> Collection:
    return db[COURSES_COLLECTION]

@router.post("/", response_model=Course)
async def create_course(course: CourseCreate, collection: Collection = Depends(get_courses_collection)):
    # 检查课程是否已存在
    if collection.find_one({"name": course.name}):
        raise HTTPException(status_code=400, detail="课程已存在")
    
    # 插入新课程
    course_dict = course.model_dump()
    result = collection.insert_one(course_dict)
    
    # 返回创建的课程
    created_course = collection.find_one({"_id": result.inserted_id})
    created_course["id"] = str(created_course["_id"])
    return created_course

@router.get("/", response_model=List[Course])
async def get_courses(skip: int = 0, limit: int = 100, collection: Collection = Depends(get_courses_collection)):
    courses = list(collection.find().skip(skip).limit(limit))
    for course in courses:
        course["id"] = str(course["_id"])
    return courses

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str, collection: Collection = Depends(get_courses_collection)):
    course = collection.find_one({"_id": course_id})
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    course["id"] = str(course["_id"])
    return course

@router.get("/department/{department}")
async def get_courses_by_department(department: str, collection: Collection = Depends(get_courses_collection)):
    courses = list(collection.find({
        "$or": [
            {"department": department},
            {"course_type": "公共选修课"}
        ]
    }))
    
    for course in courses:
        course["id"] = str(course["_id"])
    
    return courses