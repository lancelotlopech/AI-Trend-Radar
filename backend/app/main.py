from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import trends, apps, reddit, news
from app.db import Base, engine

# 创建所有数据库表 (仅在首次运行时需要，或手动通过Supabase Dashboard创建)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Trend Radar API",
    description="提供AI热点关键词、应用趋势、社交媒体讨论及新闻数据API。",
    version="1.0.0",
)

# CORS 配置，允许前端访问
origins = [
    "http://localhost:3000",
    "https://your-frontend-domain.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(trends.router, prefix="/api/trends", tags=["Trends"])
app.include_router(apps.router, prefix="/api/apps", tags=["Apps"])
app.include_router(reddit.router, prefix="/api/reddit", tags=["Reddit"])
app.include_router(news.router, prefix="/api/news", tags=["News"])

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "message": "AI Trend Radar API is running!"}

