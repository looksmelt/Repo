from pymongo import MongoClient, ASCENDING
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "student_course_system")

try:
    client = MongoClient(MONGO_URI)
    client.admin.command('ping')
    print("Connected to MongoDB successfully!")
except ConnectionFailure:
    print("Failed to connect to MongoDB")

db = client[DB_NAME]

# 创建集合引用
students_collection = db["students"]
teachers_collection = db["teachers"]
courses_collection = db["courses"]
classes_collection = db["classes"]
enrollments_collection = db["enrollments"]

# 创建索引
students_collection.create_index([("username", ASCENDING)], unique=True)
students_collection.create_index([("student_id", ASCENDING)], unique=True)
teachers_collection.create_index([("username", ASCENDING)], unique=True)
teachers_collection.create_index([("teacher_id", ASCENDING)], unique=True)
courses_collection.create_index([("name", ASCENDING)], unique=True)
enrollments_collection.create_index([("student_id", ASCENDING), ("course_id", ASCENDING)], unique=True)