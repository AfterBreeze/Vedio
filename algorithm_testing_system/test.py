from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

# 数据库配置
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "xmueducn",
    "database": "algorithm_testing_system"
}

# 初始化 FastAPI 应用
app = FastAPI()

# 数据库连接
def get_db_connection():
    return mysql.connector.connect(
        host=db_config["host"],
        user=db_config["user"],
        password=db_config["password"],
        database=db_config["database"]
    )

# 测试人员模型
class Tester(BaseModel):
    name: str
    contact_info: str

# 添加测试人员
@app.post("/testers/")
def add_tester(tester: Tester):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO testers (name, contact_info) VALUES (%s, %s)",
        (tester.name, tester.contact_info)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "测试人员添加成功"}

# 获取所有测试人员
@app.get("/testers/")
def get_testers():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM testers")
    testers = cursor.fetchall()
    cursor.close()
    conn.close()
    return testers

# 添加测试任务
class TestTask(BaseModel):
    tester_id: int
    model_id: int
    dataset_id: int
    server_id: int

@app.post("/test-tasks/")
def add_test_task(task: TestTask):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT is_occupied FROM servers WHERE id = %s", (task.server_id,))
    server = cursor.fetchone()
    if not server or server[0]:
        raise HTTPException(status_code=400, detail="服务器已被占用或不存在")

    cursor.execute(
        """
        INSERT INTO test_tasks (tester_id, model_id, dataset_id, server_id)
        VALUES (%s, %s, %s, %s)
        """,
        (task.tester_id, task.model_id, task.dataset_id, task.server_id)
    )
    cursor.execute(
        "UPDATE servers SET is_occupied = TRUE WHERE id = %s",
        (task.server_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "测试任务创建成功"}

# 获取测试任务
@app.get("/test-tasks/")
def get_test_tasks():
    conn = get_db_connection()
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

# 停止测试任务
@app.post("/test-tasks/{task_id}/stop/")
def stop_test_task(task_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT server_id FROM test_tasks WHERE id = %s", (task_id,))
    task = cursor.fetchone()
    if not task:
        raise HTTPException(status_code=404, detail="测试任务不存在")

    cursor.execute("DELETE FROM test_tasks WHERE id = %s", (task_id,))
    cursor.execute("UPDATE servers SET is_occupied = FALSE WHERE id = %s", (task[0],))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "测试任务已停止"}
