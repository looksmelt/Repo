# 在crud.py中一个简单的选课原子操作示例（假设选课关系直接存储在用户文档中）
async def select_course(student_id: str, course_id: str):
    # 检查课程是否存在且有余量
    course = await courses_collection.find_one({"_id": course_id, "status": "published", "$expr": {"$lt": ["$selected_count", "$capacity"]}})
    if not course:
        raise HTTPException(status_code=400, detail="Course not available for selection")

    # 尝试将课程ID添加到学生的已选课程列表中（使用$addToSet防止重复）
    result = await users_collection.update_one(
        {"_id": student_id, "selected_courses": {"$ne": course_id}}, # 条件：学生存在且未选过此课
        {"$addToSet": {"selected_courses": course_id}} # 操作：添加课程ID到数组
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=400, detail="Already selected this course or student not found")

    # 增加课程的已选人数
    await courses_collection.update_one({"_id": course_id}, {"$inc": {"selected_count": 1}})
    return {"message": "Course selected successfully"}