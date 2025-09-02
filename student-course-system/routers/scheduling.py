from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, time
from bson import ObjectId
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import courses_collection, classes_collection, teachers_collection
from models import ClassSchedule
from utils import get_current_teacher
import random

router = APIRouter(prefix="/scheduling", tags=["scheduling"])

# 预定义的教室列表
CLASSROOMS = ["A101", "A102", "A103", "A201", "A202", "A203", "B101", "B102", "B103"]
# 预定义的时间段
TIME_SLOTS = [
    {"start": "08:00", "end": "09:40"},
    {"start": "10:00", "end": "11:40"},
    {"start": "14:00", "end": "15:40"},
    {"start": "16:00", "end": "17:40"},
    {"start": "19:00", "end": "20:40"}
]

def is_time_overlap(schedule1, schedule2):
    # 检查两个时间段是否有重叠
    if schedule1["day_of_week"] != schedule2["day_of_week"]:
        return False
    
    def time_to_minutes(t):
        h, m = map(int, t.split(':'))
        return h * 60 + m
    
    start1 = time_to_minutes(schedule1["start_time"])
    end1 = time_to_minutes(schedule1["end_time"])
    start2 = time_to_minutes(schedule2["start_time"])
    end2 = time_to_minutes(schedule2["end_time"])
    
    return not (end1 <= start2 or end2 <= start1)

@router.post("/schedule")
async def schedule_class(schedule: ClassSchedule, current_teacher: dict = Depends(get_current_teacher)):
    # 检查课程是否存在
    course = courses_collection.find_one({"_id": ObjectId(schedule.course_id)})
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # 检查教师是否已安排该时间段
    teacher_schedules = list(classes_collection.find({"teacher_id": schedule.teacher_id}))
    for ts in teacher_schedules:
        if is_time_overlap(ts, schedule.model_dump()):
            raise HTTPException(status_code=400, detail="Teacher has another class at the same time")
    
    # 检查教室是否已被占用
    classroom_schedules = list(classes_collection.find({"classroom": schedule.classroom}))
    for cs in classroom_schedules:
        if is_time_overlap(cs, schedule.model_dump()):
            raise HTTPException(status_code=400, detail="Classroom is occupied at the same time")
    
    # 创建排课记录
    schedule_dict = schedule.model_dump()
    schedule_dict["created_at"] = datetime.now()
    
    result = classes_collection.insert_one(schedule_dict)
    
    # 更新课程信息
    courses_collection.update_one(
        {"_id": ObjectId(schedule.course_id)},
        {"$set": {"schedule": schedule_dict, "updated_at": datetime.now()}}
    )
    
    return {"id": str(result.inserted_id), "message": "Class scheduled successfully"}

@router.post("/auto-schedule")
async def auto_schedule_classes(current_teacher: dict = Depends(get_current_teacher)):
    # 获取所有未安排课程的课程
    unscheduled_courses = list(courses_collection.find({"schedule": None, "teacher_id": {"$ne": None}}))
    
    scheduled = 0
    conflicts = 0
    
    for course in unscheduled_courses:
        teacher_id = course["teacher_id"]
        teacher = teachers_collection.find_one({"_id": ObjectId(teacher_id)})
        
        if not teacher:
            continue
        
        # 获取教师已有的课程安排
        teacher_schedules = list(classes_collection.find({"teacher_id": teacher_id}))
        
        # 尝试为课程安排时间
        scheduled_successfully = False
        
        for day in range(1, 8):  # 周一到周日
            for time_slot in TIME_SLOTS:
                for classroom in CLASSROOMS:
                    # 创建临时排课对象
                    potential_schedule = {
                        "course_id": str(course["_id"]),
                        "teacher_id": teacher_id,
                        "classroom": classroom,
                        "day_of_week": day,
                        "start_time": time_slot["start"],
                        "end_time": time_slot["end"]
                    }
                    
                    # 检查教师时间冲突
                    teacher_conflict = False
                    for ts in teacher_schedules:
                        if is_time_overlap(ts, potential_schedule):
                            teacher_conflict = True
                            break
                    
                    if teacher_conflict:
                        continue
                    
                    # 检查教室时间冲突
                    classroom_schedules = list(classes_collection.find({"classroom": classroom}))
                    classroom_conflict = False
                    for cs in classroom_schedules:
                        if is_time_overlap(cs, potential_schedule):
                            classroom_conflict = True
                            break
                    
                    if classroom_conflict:
                        continue
                    
                    # 没有冲突，安排课程
                    schedule_dict = {
                        "course_id": str(course["_id"]),
                        "teacher_id": teacher_id,
                        "classroom": classroom,
                        "day_of_week": day,
                        "start_time": time_slot["start"],
                        "end_time": time_slot["end"],
                        "created_at": datetime.now()
                    }
                    
                    classes_collection.insert_one(schedule_dict)
                    
                    # 更新课程信息
                    courses_collection.update_one(
                        {"_id": course["_id"]},
                        {"$set": {"schedule": schedule_dict, "updated_at": datetime.now()}}
                    )
                    
                    scheduled += 1
                    scheduled_successfully = True
                    break
                
                if scheduled_successfully:
                    break
            
            if scheduled_successfully:
                break
        
        if not scheduled_successfully:
            conflicts += 1
    
    return {
        "message": f"Auto-scheduling completed. Scheduled: {scheduled}, Conflicts: {conflicts}",
        "scheduled": scheduled,
        "conflicts": conflicts
    }

@router.get("/teacher/{teacher_id}")
async def get_teacher_schedule(teacher_id: str):
    schedules = list(classes_collection.find({"teacher_id": teacher_id}))
    
    for schedule in schedules:
        schedule["id"] = str(schedule["_id"])
    
    return schedules

@router.get("/classroom/{classroom}")
async def get_classroom_schedule(classroom: str):
    schedules = list(classes_collection.find({"classroom": classroom}))
    
    for schedule in schedules:
        schedule["id"] = str(schedule["_id"])
    
    return schedules