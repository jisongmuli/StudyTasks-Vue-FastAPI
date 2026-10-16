"""学习任务清单：所有后端业务都放在这个文件里，便于第一次阅读。"""

from itertools import count

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field, field_validator

# 1. 创建应用。可以类比成 Spring Boot 项目的 Web 应用入口。
app = FastAPI(title="学习任务清单 API", description="一个用于学习前后端通信的小项目。")


# 2. 定义数据格式。可以类比 Java 的 DTO：规定字段和校验规则。
class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=80)

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("任务内容不能全是空格")
        return value


class TaskUpdate(BaseModel):
    completed: bool


class Task(BaseModel):
    id: int
    title: str
    completed: bool = False


# 3. 暂时用 Python 列表保存数据。重启后端后会恢复下面的示例任务。
# 数据库、Service、Repository 等分层可以在读懂这个版本后再逐步加入。
tasks = [
    Task(id=1, title="跑起来，添加自己的第一条学习任务"),
    Task(id=2, title="打开接口文档，试一次 GET 请求"),
    Task(id=3, title="找到 App.vue，修改页面标题"),
]
task_ids = count(4)


def find_task(task_id: int) -> Task:
    for task in tasks:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="任务不存在，请刷新列表")


# 4. 定义接口。装饰器把“HTTP 方法 + 路径”关联到一个 Python 函数。
# 接口函数可以类比 Spring Boot Controller 中的方法。
@app.get("/api/tasks", response_model=list[Task])
async def list_tasks():
    """查看所有任务。"""
    return tasks


@app.post("/api/tasks", response_model=Task, status_code=201)
async def create_task(body: TaskCreate):
    """接收 JSON 内容，创建任务，并返回新任务。"""
    task = Task(id=next(task_ids), title=body.title)
    tasks.append(task)
    return task


@app.patch("/api/tasks/{task_id}", response_model=Task)
async def update_task(task_id: int, body: TaskUpdate):
    """按任务 ID 修改完成状态。"""
    task = find_task(task_id)
    task.completed = body.completed
    return task


@app.delete("/api/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    """按任务 ID 删除任务。204 表示成功，但没有返回内容。"""
    task = find_task(task_id)
    tasks.remove(task)
    return Response(status_code=204)
