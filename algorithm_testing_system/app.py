from fastapi import FastAPI
from database import initialize_database
from routers import testers, tasks, resources

# 创建 FastAPI 实例
app = FastAPI()

# 加载路由
app.include_router(testers.router, prefix="/testers", tags=["Testers"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])
app.include_router(resources.router, prefix="/resources", tags=["Resources"])

# 初始化数据库
initialize_database()

@app.get("/")
def root():
    return {"message": "智能算法测试系统 API"}
