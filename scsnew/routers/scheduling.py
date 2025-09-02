from fastapi import APIRouter, HTTPException, Depends
from pymongo.collection import Collection
from database import db, SCHEDULES_COLLECTION, CLASSROOMS_COLLECTION
from models import Schedule, ScheduleCreate
from typing import List

router = APIRouter(prefix="/schedules", tags=["scheduling"])

def get_schedules_collection() -> Collection:
    return db[SCHEDULES_COLLECTION]

def get_classrooms_collection() -> Collection:
    return db[CLASSROOMS_COLLECTION]

@router.post("/", response_model=Schedule)
async def create_schedule(schedule: ScheduleCreate, 
                         schedules_collection: Collection = Depends(get_schedules_collection),
                         classrooms_collection: Collection = Depends(get_classrooms_collection)):
    # 检查教室是否存在
    classroom = classrooms_collection.find_one({"id": schedule.classroom})
    if not classroom:
        raise HTTPException(status_code=404, detail="教室不存在")
    
    # 检查时间冲突 - 同一教师同一时间不能上不同课程
    teacher_conflict = schedules_collection.find_one({
        "teacher_id": schedule.teacher_id,
        "day_of_week": schedule.day_of_week,
        "$or": [
            {
                "start_time": {"$lt": schedule.end_time},
                "end_time": {"$gt": schedule.start_time}
            }
        ]
    })
    
    if teacher_conflict:
        raise HTTPException(status_code=400, detail="教师在该时间段已有其他课程安排")
    
    # 检查时间冲突 - 同一教室同一时间不能安排不同课程
    classroom_conflict = schedules_collection.find_one({
        "classroom": schedule.classroom,
        "day_of_week": schedule.day_of_week,
        "$or": [
            {
                "start_time": {"$lt": schedule.end_time},
                "end_time": {"$gt": schedule.start_time}
            }
        ]
    })
    
    if classroom_conflict:
        raise HTTPException(status_code=400, detail="教室在该时间段已被占用")
    
    # 插入新排课
    schedule_dict = schedule.model_dump()
    result = schedules_collection.insert_one(schedule_dict)
    
    # 返回创建的排课
    created_schedule = schedules_collection.find_one({"_id": result.inserted_id})
    created_schedule["id"] = str(created_schedule["_id"])
    return created_schedule

@router.get("/", response_model=List[Schedule])
async def get_schedules(skip: int = 0, limit: int = 100, collection: Collection = Depends(get_schedules_collection)):
    schedules = list(collection.find().skip(skip).limit(limit))
    for schedule in schedules:
        schedule["id"] = str(schedule["_id"])
    return schedules

@router.get("/teacher/{teacher_id}", response_model=List[Schedule])
async def get_teacher_schedule(teacher_id: str, collection: Collection = Depends(get_schedules_collection)):
    schedules = list(collection.find({"teacher_id": teacher_id}))
    for schedule in schedules:
        schedule["id"] = str(schedule["_id"])
    return schedules

@router.get("/classroom/{classroom}", response_model=List[Schedule])
async def get_classroom_schedule(classroom: str, collection: Collection = Depends(get_schedules_collection)):
    schedules = list(collection.find({"classroom": classroom}))
    for schedule in schedules:
        schedule["id"] = str(schedule["_id"])
    return schedules