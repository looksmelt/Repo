from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import students, teachers, courses, scheduling
from database import client
import os
import uvicorn
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    print("Starting Student Course System...")
    yield 
    # 关闭时执行
    client.close()
    print("Student Course System shut down.")

app = FastAPI(
    title="Student Course System",
    version="1.0.0",
    lifespan=lifespan
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(courses.router)
app.include_router(scheduling.router)

@app.get("/")
async def root():
    return {"message": "Student Course System API"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)



#     MONGO_URI=mongodb://localhost:27017
# DB_NAME=student_course_system
# SECRET_KEY=your-super-secret-key-change-this-in-production
