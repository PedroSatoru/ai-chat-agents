import os
import certifi
from dotenv import load_dotenv
from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    user = os.getenv("DB_USER") or os.getenv("USER")
    password = os.getenv("DB_PASSWORD") or os.getenv("PASSWORD")
    host = os.getenv("DB_HOST") or os.getenv("HOST")
    port = os.getenv("DB_PORT") or os.getenv("PORT")
    dbname = os.getenv("DB_NAME") or os.getenv("DBNAME")

    if all([user, password, host, port, dbname]):
        encoded_password = quote_plus(str(password))
        DATABASE_URL = f"postgresql+psycopg2://{user}:{encoded_password}@{host}:{port}/{dbname}?sslmode=require"
    else:
        DATABASE_URL = "sqlite:///./app.db"


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "chat_db"
    MONGO_CONVERSATIONS_COLLECTION: str = "chat_conversations"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
mongo_client_kwargs = {}

if settings.MONGO_URI.startswith("mongodb+srv://"):
    mongo_client_kwargs["tlsCAFile"] = certifi.where()

mongo_client = AsyncIOMotorClient(settings.MONGO_URI, **mongo_client_kwargs)
mongo_db = mongo_client[settings.MONGO_DB]
