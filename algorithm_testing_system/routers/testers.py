from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection

router = APIRouter()

# 测试人员数据模型
class Tester(BaseModel):
    name: str
    contact_info: str

# 添加测试人员
@router.post("/")
def add_tester(tester: Tester):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO testers (name, contact_info) VALUES (%s, %s)", (tester.name, tester.contact_info))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "测试人员添加成功"}

# 获取所有测试人员
@router.get("/")
def get_testers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM testers")
    testers = cursor.fetchall()
    cursor.close()
    conn.close()
    return testers
