from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime
from bson import ObjectId
from database import courses_collection, teachers_collection
from models import CourseCreate, Course
from utils import get_current_teacher, get_current_student
from typing import List

router = APIRouter(prefix="/courses", tags=["courses"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_course(course: CourseCreate, current_teacher: dict = Depends(get_current_teacher)):
    # 检查课程名称是否已存在
    if courses_collection.find_one({"name": course.name}):
        raise HTTPException(status_code=400, detail="Course name already exists")
    
    course_dict = course.model_dump()
    course_dict["created_at"] = datetime.now()
    course_dict["updated_at"] = datetime.now()
    course_dict["teacher_id"] = None
    course_dict["schedule"] = None
    
    result = courses_collection.insert_one(course_dict)
    return {"id": str(result.inserted_id), "message": "Course created successfully"}

@router.get("/", response_model=List[Course])
async def get_courses(course_type: str = None, department: str = None, 
                     class_name: str = None, current_student: dict = Depends(get_current_student)):
    query = {}
    if course_type:
        query["course_type"] = course_type
    if department:
        query["department"] = department
    if class_name:
        query["class_name"] = class_name
    
    # 对于学生，只显示适合他们的课程
    if current_student:
        # 公共选修课对所有学生开放
        public_courses = {"course_type": "public_elective"}
        
        # 专业必修课只对相应院系和班级的学生开放
        required_courses = {
            "course_type": "required",
            "department": current_student["department"],
            "class_name": current_student["class_name"]
        }
        
        query = {"$or": [public_courses, required_courses]}
    
    courses = list(courses_collection.find(query))
    
    for course in courses:
        course["id"] = str(course["_id"])
    
    return courses

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str):
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course["id"] = str(course["_id"])
    return course

@router.put("/{course_id}/assign/{teacher_id}")
async def assign_teacher_to_course(course_id: str, teacher_id: str, 
                                  current_teacher: dict = Depends(get_current_teacher)):
    # 检查课程是否存在
    course = courses_collection.find_one({"_id": ObjectId(course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # 检查教师是否存在
    teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
    if not teacher:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # 更新课程信息
    courses_collection.update_one(
        {"_id": ObjectId(course_id)},
        {"$set": {"teacher_id": teacher_id, "updated_at": datetime.now()}}
    )
    
    # 更新教师信息
    teachers_collection.update_one(
        {"_id": ObjectId(teacher_id)},
        {"$addToSet": {"courses": course_id}, "$set": {"updated_at": datetime.now()}}
    )
    
    return {"message": "Teacher assigned to course successfully"}