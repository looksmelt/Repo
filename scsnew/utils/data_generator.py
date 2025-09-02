import random
from faker import Faker
from datetime import time
from typing import List, Dict, Any
import json

fake = Faker('zh_CN')

# 预定义数据
DEPARTMENTS = [
    "计算机科学与技术", "电子信息工程", "机械工程", "土木工程", "生物医学工程",
    "经济学", "管理学", "法学", "文学", "艺术设计"
]

PUBLIC_COURSES = [
    "思想道德修养与法律基础", "演讲与口才", "大学英语", "高等数学", "大学物理",
    "计算机基础", "体育", "军事理论", "职业生涯规划", "创新创业基础"
]

CLASSROOM_PREFIXES = ["A", "B", "C", "D", "E"]
CLASSROOM_FLOORS = [1, 2, 3, 4, 5]
CLASSROOM_NUMBERS = [f"{i:02d}" for i in range(1, 21)]

def generate_departments() -> List[Dict[str, Any]]:
    return [{"name": dept} for dept in DEPARTMENTS]

def generate_classrooms() -> List[Dict[str, Any]]:
    classrooms = []
    for prefix in CLASSROOM_PREFIXES:
        for floor in CLASSROOM_FLOORS:
            for number in CLASSROOM_NUMBERS[:8]:  # 每层8个教室
                classroom_id = f"{prefix}{floor}{number}"
                capacity = random.randint(30, 120)
                classrooms.append({
                    "id": classroom_id,
                    "capacity": capacity,
                    "building": prefix,
                    "floor": floor
                })
    return classrooms

def generate_students(count: int = 20000) -> List[Dict[str, Any]]:
    students = []
    classes_per_dept = 40  # 每个院系40个班级
    
    for i in range(count):
        dept_index = i % len(DEPARTMENTS)
        department = DEPARTMENTS[dept_index]
        class_num = (i % classes_per_dept) + 1
        class_name = f"{department}{class_num:02d}班"
        
        gender = random.choice(["男", "女"])
        if gender == "男":
            name = fake.name_male()
        else:
            name = fake.name_female()
            
        student = {
            "username": f"student{i+1:06d}",
            "password": "password123",  # 默认密码，实际应用中应该加密
            "nickname": f"学生{i+1}",
            "signature": fake.sentence(),
            "name": name,
            "student_id": f"2024{(dept_index+1):02d}{(i % 1000):04d}",
            "department": department,
            "class_name": class_name,
            "gender": gender,
            "age": random.randint(18, 25),
            "phone": fake.phone_number(),
            "email": f"student{i+1}@example.com",
            "address": fake.address(),
            "current_grades": {},
            "past_grades": {}
        }
        students.append(student)
    return students

def generate_teachers(count: int = 200) -> List[Dict[str, Any]]:
    teachers = []
    for i in range(count):
        gender = random.choice(["男", "女"])
        if gender == "男":
            name = fake.name_male()
        else:
            name = fake.name_female()
            
        teacher = {
            "username": f"teacher{i+1:04d}",
            "password": "password123",  # 默认密码，实际应用中应该加密
            "nickname": f"教师{i+1}",
            "signature": fake.sentence(),
            "name": name,
            "teacher_id": f"T{(i+1):04d}",
            "gender": gender,
            "age": random.randint(28, 65),
            "phone": fake.phone_number(),
            "email": f"teacher{i+1}@example.com",
            "address": fake.address(),
            "courses": []
        }
        teachers.append(teacher)
    return teachers

def generate_courses() -> List[Dict[str, Any]]:
    courses = []
    
    # 公共选修课
    for i, course_name in enumerate(PUBLIC_COURSES):
        course = {
            "name": course_name,
            "description": f"{course_name}课程描述",
            "course_type": "公共选修课",
            "department": None,
            "class_names": None,
            "teacher_id": None
        }
        courses.append(course)
    
    # 专业必修课 (每个院系9门专业课程)
    professional_courses = [
        "专业导论", "专业核心课程1", "专业核心课程2", "专业核心课程3",
        "专业核心课程4", "专业核心课程5", "专业核心课程6", "专业实践", "毕业设计"
    ]
    
    for dept in DEPARTMENTS:
        for i, course_name in enumerate(professional_courses):
            course = {
                "name": f"{dept}{course_name}",
                "description": f"{dept}{course_name}课程描述",
                "course_type": "专业必修课",
                "department": dept,
                "class_names": [f"{dept}{j:02d}班" for j in range(1, 41)],
                "teacher_id": None
            }
            courses.append(course)
    
    return courses

def generate_time_slots():
    """生成上课时间段"""
    time_slots = []
    days_of_week = list(range(1, 8))  # 1-7代表周一到周日
    
    # 上午
    for day in days_of_week:
        time_slots.append({
            "day_of_week": day,
            "start_time": "08:00",
            "end_time": "09:40"
        })
        time_slots.append({
            "day_of_week": day,
            "start_time": "10:00",
            "end_time": "11:40"
        })
    
    # 下午
    for day in days_of_week:
        time_slots.append({
            "day_of_week": day,
            "start_time": "14:00",
            "end_time": "15:40"
        })
        time_slots.append({
            "day_of_week": day,
            "start_time": "16:00",
            "end_time": "17:40"
        })
    
    # 晚上
    for day in days_of_week[:5]:  # 周一到周五晚上
        time_slots.append({
            "day_of_week": day,
            "start_time": "19:00",
            "end_time": "20:40"
        })
    
    return time_slots

def assign_courses_to_teachers(teachers: List[Dict[str, Any]], courses: List[Dict[str, Any]]):
    """为教师分配课程"""
    # 分离公共课和专业课
    public_courses = [c for c in courses if c["course_type"] == "公共选修课"]
    professional_courses = [c for c in courses if c["course_type"] == "专业必修课"]
    
    # 分配公共课
    public_teachers = teachers[:50]  # 前50位教师教授公共课
    for i, course in enumerate(public_courses):
        teacher = public_teachers[i % len(public_teachers)]
        course["teacher_id"] = teacher["teacher_id"]
        teacher["courses"].append(course["name"])
    
    # 分配专业课
    dept_teachers = {}
    for teacher in teachers[50:]:
        dept = random.choice(DEPARTMENTS)
        if dept not in dept_teachers:
            dept_teachers[dept] = []
        dept_teachers[dept].append(teacher)
    
    for course in professional_courses:
        dept = course["department"]
        if dept in dept_teachers and dept_teachers[dept]:
            teacher = random.choice(dept_teachers[dept])
            course["teacher_id"] = teacher["teacher_id"]
            teacher["courses"].append(course["name"])
    
    return teachers, courses

def generate_schedules(teachers: List[Dict[str, Any]], courses: List[Dict[str, Any]], classrooms: List[Dict[str, Any]]):
    """生成课程安排，确保没有时间冲突"""
    schedules = []
    time_slots = generate_time_slots()
    classroom_ids = [c["id"] for c in classrooms]
    
    # 记录教师和教室的时间占用
    teacher_occupied = {t["teacher_id"]: set() for t in teachers}
    classroom_occupied = {c["id"]: set() for c in classrooms}
    
    for course in courses:
        if not course["teacher_id"]:
            continue  # 没有分配教师的课程跳过
            
        teacher_id = course["teacher_id"]
        
        # 尝试分配时间 slot 和教室
        assigned = False
        random.shuffle(time_slots)
        random.shuffle(classroom_ids)
        
        for slot in time_slots:
            if assigned:
                break
                
            time_key = (slot["day_of_week"], slot["start_time"], slot["end_time"])
            
            # 检查教师是否有空
            if time_key in teacher_occupied[teacher_id]:
                continue
                
            # 检查教室是否有空
            for classroom_id in classroom_ids:
                if time_key in classroom_occupied[classroom_id]:
                    continue
                    
                # 分配成功
                schedule = {
                    "course_id": course["name"],
                    "teacher_id": teacher_id,
                    "classroom": classroom_id,
                    "day_of_week": slot["day_of_week"],
                    "start_time": slot["start_time"],
                    "end_time": slot["end_time"]
                }
                schedules.append(schedule)
                
                # 更新占用记录
                teacher_occupied[teacher_id].add(time_key)
                classroom_occupied[classroom_id].add(time_key)
                
                assigned = True
                break
    
    return schedules

def generate_all_data():
    """生成所有数据"""
    print("生成院系数据...")
    departments = generate_departments()
    
    print("生成教室数据...")
    classrooms = generate_classrooms()
    
    print("生成学生数据...")
    students = generate_students(20000)
    
    print("生成教师数据...")
    teachers = generate_teachers(200)
    
    print("生成课程数据...")
    courses = generate_courses()
    
    print("为教师分配课程...")
    teachers, courses = assign_courses_to_teachers(teachers, courses)
    
    print("生成课程安排...")
    schedules = generate_schedules(teachers, courses, classrooms)
    
    return {
        "departments": departments,
        "classrooms": classrooms,
        "students": students,
        "teachers": teachers,
        "courses": courses,
        "schedules": schedules
    }