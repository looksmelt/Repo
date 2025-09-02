# app/main.py
from fastapi import FastAPI
from app.database import client
from app.routes import auth, courses, users, enrollments  # 导入你的路由

app = FastAPI(title="Student Course Selection System")

# 包含路由
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(courses.router, prefix="/courses", tags=["courses"])
app.include_router(enrollments.router, prefix="/enrollments", tags=["enrollments"])

@app.on_event("startup")
async def startup_db_client():
    # 可以在这里进行数据库索引创建等操作
    await client.start_session()

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()