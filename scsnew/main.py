from fastapi import FastAPI, Depends
from pymongo.collection import Collection
from .database import db, STUDENTS_COLLECTION, TEACHERS_COLLECTION, COURSES_COLLECTION, SCHEDULES_COLLECTION, DEPARTMENTS_COLLECTION, CLASSROOMS_COLLECTION
from routers import students, teachers, courses, scheduling
from utils.data_generator import generate_all_data
import uvicorn

app = FastAPI(title="学生选课系统", description="基于FastAPI和MongoDB的学生选课系统API")

# 包含路由
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(courses.router)
app.include_router(scheduling.router)

@app.get("/")
async def root():
    return {"message": "欢迎使用学生选课系统API"}

@app.post("/initialize-data")
async def initialize_data():
    """初始化数据端点 - 生成并插入测试数据"""
    try:
        # 生成所有数据
        data = generate_all_data()
        
        # 获取集合
        students_collection = db[STUDENTS_COLLECTION]
        teachers_collection = db[TEACHERS_COLLECTION]
        courses_collection = db[COURSES_COLLECTION]
        schedules_collection = db[SCHEDULES_COLLECTION]
        departments_collection = db[DEPARTMENTS_COLLECTION]
        classrooms_collection = db[CLASSROOMS_COLLECTION]
        
        # 清空现有数据
        students_collection.delete_many({})
        teachers_collection.delete_many({})
        courses_collection.delete_many({})
        schedules_collection.delete_many({})
        departments_collection.delete_many({})
        classrooms_collection.delete_many({})
        
        # 插入新数据
        departments_collection.insert_many(data["departments"])
        classrooms_collection.insert_many(data["classrooms"])
        students_collection.insert_many(data["students"])
        teachers_collection.insert_many(data["teachers"])
        courses_collection.insert_many(data["courses"])
        schedules_collection.insert_many(data["schedules"])
        
        return {
            "message": "数据初始化成功",
            "counts": {
                "departments": len(data["departments"]),
                "classrooms": len(data["classrooms"]),
                "students": len(data["students"]),
                "teachers": len(data["teachers"]),
                "courses": len(data["courses"]),
                "schedules": len(data["schedules"])
            }
        }
    except (ValueError, KeyError, TypeError) as e:  # Replace with specific exceptions
        return {"message": f"数据初始化失败: {str(e)}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)