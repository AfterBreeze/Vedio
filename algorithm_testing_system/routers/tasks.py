from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection

router = APIRouter()

# 测试任务模型
class TestTask(BaseModel):
    tester_id: int
    model_id: int
    dataset_id: int
    server_id: int

# 创建测试任务
@router.post("/")
def add_test_task(task: TestTask):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_occupied FROM servers WHERE id = %s", (task.server_id,))
    server = cursor.fetchone()
    if not server or server[0]:
        raise HTTPException(status_code=400, detail="服务器已被占用或不存在")

    cursor.execute("""
        INSERT INTO test_tasks (tester_id, model_id, dataset_id, server_id)
        VALUES (%s, %s, %s, %s)
    """, (task.tester_id, task.model_id, task.dataset_id, task.server_id))
    cursor.execute("UPDATE servers SET is_occupied = TRUE WHERE id = %s", (task.server_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "测试任务创建成功"}

# 查看所有测试任务
@router.get("/")
def get_test_tasks():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT tt.id, t.name AS tester, m.name AS model, d.name AS dataset, s.model AS server, tt.test_status
        FROM test_tasks tt
        JOIN testers t ON tt.tester_id = t.id
        JOIN models m ON tt.model_id = m.id
        JOIN datasets d ON tt.dataset_id = d.id
        JOIN servers s ON tt.server_id = s.id
    """)
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return tasks
