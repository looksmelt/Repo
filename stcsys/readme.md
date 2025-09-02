# 学生课程系统 API 文档

## 概述
本系统基于 **FastAPI** 构建，提供学生和教师的课程管理、选课、用户认证等 RESTful API。支持两种用户角色，并采用 JWT 令牌进行身份验证和授权。

---

## 功能特性

- **用户管理**：学生/教师注册与登录
- **身份验证**：JWT 安全认证
- **课程管理**：课程创建、查询、分配教师
- **选课系统**：学生选课、课程容量控制
- **数据生成**：测试数据生成工具
- **CORS 支持**：跨域请求

---

## 技术栈

- 后端框架：FastAPI
- 数据库：MongoDB
- 认证：JWT
- 密码加密：bcrypt
- CORS：跨域资源共享

---

## 安装与运行

### 环境要求

- Python 3.7+
- MongoDB
- 依赖包见 `requirements.txt` 

### 安装步骤

1. 克隆项目并安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

2. 配置环境变量：

    新建 `.env` 文件，设置如下：

    ```
    SECRET_KEY=your-secret-key-here
    MONGODB_URI=your-mongodb-connection-string
    ```

3. 运行应用：

    ```bash
    uvicorn main:app --reload 
    ```

4. 访问 API 文档：

    浏览器打开 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API 端点

### 认证相关

- `POST /students/register`：学生注册
- `POST /teachers/register`：教师注册
- `POST /login`：用户登录

### 课程相关

- `POST /courses`：创建课程（教师权限）
- `GET /courses`：获取课程列表
- `PUT /courses/{course_id}/assign/{teacher_id}`：分配教师

### 用户相关

- `GET /students/me`：当前学生信息
- `GET /teachers/me`：当前教师信息
- `GET /students/me/courses`：学生已选课程
- `POST /students/me/enroll/{course_id}`：学生选课

### 工具端点

- `POST /generate-data`：生成测试数据
- `GET /`：根端点，欢迎信息

---

## 数据模型

### Student (学生)

| 字段         | 说明         |
| ------------ | ------------ |
| id           | 唯一标识     |
| username     | 用户名       |
| password     | 密码（加密） |
| student_id   | 学号         |
| full_name    | 全名         |
| email        | 邮箱         |
| major        | 专业         |
| created_at   | 创建时间     |
| updated_at   | 更新时间     |

### Teacher (教师)

| 字段         | 说明         |
| ------------ | ------------ |
| id           | 唯一标识     |
| username     | 用户名       |
| password     | 密码（加密） |
| teacher_id   | 教师编号     |
| full_name    | 全名         |
| email        | 邮箱         |
| department   | 部门         |
| courses      | 所授课程列表 |
| created_at   | 创建时间     |
| updated_at   | 更新时间     |

### Course (课程)

| 字段         | 说明         |
| ------------ | ------------ |
| id           | 唯一标识     |
| name         | 课程名称     |
| description  | 课程描述     |
| schedule     | 课程安排     |
| capacity     | 课程容量     |
| teacher_id   | 授课教师ID   |
| created_at   | 创建时间     |
| updated_at   | 更新时间     |

### Enrollment (选课关系)

| 字段         | 说明         |
| ------------ | ------------ |
| student_id   | 学生ID       |
| course_id    | 课程ID       |
| teacher_id   | 教师ID       |
| enrolled_at  | 选课时间     |

---

## 身份验证

- 登录后获取 JWT 令牌
- 后续请求需在 `Authorization` 头中携带：`Bearer {token}`
- 令牌有效期：30分钟

---

## 权限控制

- 学生端点：需学生令牌
- 教师端点：需教师令牌
- 公共端点：无需认证

---

## 错误处理

- 标准 HTTP 状态码：
  - 200：成功
  - 201：资源创建
  - 400：参数错误
  - 401：未授权
  - 403：权限不足
  - 404：资源不存在
  - 500：服务器错误

- 错误响应格式：

  ```json
  {
     "detail": "错误描述信息"
  }
  ```

---

## 示例请求

### 学生注册

```bash
curl -X POST "http://localhost:8000/students/register" \
-H "Content-Type: application/json" \
-d '{
  "username": "student1",
  "password": "password123",
  "student_id": "S1001",
  "full_name": "张三",
  "email": "zhangsan@example.com",
  "major": "计算机科学"
}'
用户登录
bash
curl -X POST "http://localhost:8000/login" \
-H "Content-Type: application/json" \
-d '{
  "username": "student1",
  "password": "password123"
}'
响应示例：

json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
获取当前学生信息
bash
curl -X GET "http://localhost:8000/students/me" \
-H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
注意事项
确保 MongoDB 服务正在运行

生产环境中应使用更强的密钥和更严格的安全设置

密码使用 bcrypt 加密存储，不会明文保存

课程有容量限制，选课人数达到上限后将无法继续选课

每个课程必须分配教师后学生才能选课

开发说明
项目结构：

text
├── main.py          # 主应用文件
├── database.py      # 数据库连接配置
├── models.py        # Pydantic 模型定义
├── data_generator.py # 测试数据生成器
└── .env            # 环境变量配置文件
如需扩展功能，可参考 FastAPI 官方文档和 MongoDB 驱动程序文档。