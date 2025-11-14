import os
from dotenv import load_dotenv
from app.services.core.config import settings

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    # 其他配置，如API密钥等

settings = Settings()

