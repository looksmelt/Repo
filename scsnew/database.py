from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "student_course_system"

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client[DB_NAME]

# 集合名称
STUDENTS_COLLECTION = "students"
TEACHERS_COLLECTION = "teachers"
COURSES_COLLECTION = "courses"
SCHEDULES_COLLECTION = "schedules"
DEPARTMENTS_COLLECTION = "departments"
CLASSROOMS_COLLECTION = "classrooms"

# 创建索引
def create_indexes():
    # 学生集合索引
    db[STUDENTS_COLLECTION].create_index("username", unique=True)
    db[STUDENTS_COLLECTION].create_index("student_id", unique=True)
    db[STUDENTS_COLLECTION].create_index("email", unique=True)
    
    # 教师集合索引
    db[TEACHERS_COLLECTION].create_index("username", unique=True)
    db[TEACHERS_COLLECTION].create_index("teacher_id", unique=True)
    db[TEACHERS_COLLECTION].create_index("email", unique=True)
    
    # 课程集合索引
    db[COURSES_COLLECTION].create_index("name")
    
    # 排课集合索引
    db[SCHEDULES_COLLECTION].create_index("teacher_id")
    db[SCHEDULES_COLLECTION].create_index("classroom")
    db[SCHEDULES_COLLECTION].create_index([("day_of_week", 1), ("start_time", 1), ("end_time", 1)])

# 调用创建索引
create_indexes()