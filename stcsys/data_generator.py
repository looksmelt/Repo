from faker import Faker
from datetime import datetime
import random
from database import students_collection, teachers_collection, courses_collection
import bcrypt

fake = Faker('zh_CN')

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def generate_students(count=50):
    """生成学生数据"""
    students = []
    used_student_ids = set()
    used_usernames = set()
    
    for i in range(count):
        while True:
            student_id = f"{fake.random_int(2020, 2023)}{fake.random_int(1000, 9999)}"
            if student_id not in used_student_ids:
                used_student_ids.add(student_id)
                break
        
        while True:
            username = f"stu_{fake.user_name()}"
            if username not in used_usernames:
                used_usernames.add(username)
                break
        
        gender = random.choice(["male", "female"])
        if gender == "male":
            name = fake.name_male()
        else:
            name = fake.name_female()
        
        student = {
            "username": username,
            "password": hash_password("password123"),
            "nickname": fake.user_name(),
            "signature": fake.sentence(),
            "name": name,
            "student_id": student_id,
            "gender": gender,
            "age": fake.random_int(18, 25),
            "phone": fake.phone_number(),
            "email": fake.email(),
            "address": fake.address(),
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        students.append(student)
    
    if students:
        students_collection.insert_many(students)
        print(f"Generated {len(students)} students")
    return students

def generate_teachers(count=5):
    """生成教师数据"""
    teachers = []
    used_teacher_ids = set()
    used_usernames = set()
    
    for i in range(count):
        while True:
            teacher_id = f"T{fake.random_int(1000, 9999)}"
            if teacher_id not in used_teacher_ids:
                used_teacher_ids.add(teacher_id)
                break
        
        while True:
            username = f"tea_{fake.user_name()}"
            if username not in used_usernames:
                used_usernames.add(username)
                break
        
        gender = random.choice(["male", "female"])
        if gender == "male":
            name = fake.name_male()
        else:
            name = fake.name_female()
        
        teacher = {
            "username": username,
            "password": hash_password("password123"),
            "name": name,
            "teacher_id": teacher_id,
            "gender": gender,
            "age": fake.random_int(28, 65),
            "phone": fake.phone_number(),
            "email": fake.email(),
            "courses": [],
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        teachers.append(teacher)
    
    if teachers:
        teachers_collection.insert_many(teachers)
        print(f"Generated {len(teachers)} teachers")
    return teachers

def generate_courses(count=5):
    """生成课程数据"""
    courses = []
    course_names = [
        "高等数学", "大学英语", "计算机基础", 
        "程序设计", "数据结构"
    ]
    
    for i in range(min(count, len(course_names))):
        course = {
            "name": course_names[i],
            "description": fake.paragraph(),
            "credits": round(random.uniform(1.0, 5.0), 1),
            "capacity": fake.random_int(30, 100),
            "teacher_id": None,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        courses.append(course)
    
    if courses:
        courses_collection.insert_many(courses)
        print(f"Generated {len(courses)} courses")
    return courses

def assign_teachers_to_courses():
    """为课程分配教师"""
    teachers = list(teachers_collection.find())
    courses = list(courses_collection.find())
    
    if not teachers or not courses:
        print("No teachers or courses to assign")
        return
    
    # 确保每个教师至少教授一门课程
    for i, course in enumerate(courses):
        teacher = teachers[i % len(teachers)]
        
        # 更新课程信息
        courses_collection.update_one(
            {"_id": course["_id"]},
            {"$set": {"teacher_id": str(teacher["_id"]), "updated_at": datetime.now()}}
        )
        
        # 更新教师信息
        teachers_collection.update_one(
            {"_id": teacher["_id"]},
            {"$addToSet": {"courses": str(course["_id"])}, "$set": {"updated_at": datetime.now()}}
        )
    
    print("Assigned teachers to courses")

def generate_all_data():
    """生成所有数据"""
    print("Starting data generation...")
    
    # 清空现有数据
    students_collection.delete_many({})
    teachers_collection.delete_many({})
    courses_collection.delete_many({})
    
    # 生成新数据
    generate_students(50)
    generate_teachers(5)
    generate_courses(5)
    assign_teachers_to_courses()
    
    print("Data generation completed!")

if __name__ == "__main__":
    generate_all_data()