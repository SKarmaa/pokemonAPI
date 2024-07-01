from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import yaml
from dotenv import load_dotenv
import os
from typing import AsyncGenerator

load_dotenv()

with open("config.yaml", "r") as f:
    config: dict = yaml.safe_load(f)

DATABASE_URL: str = config["database"]["url"].format(
    DB_USER=os.getenv("DB_USER"),
    DB_PASSWORD=os.getenv("DB_PASSWORD"),
    DB_HOST=os.getenv("DB_HOST"),
    DB_PORT=os.getenv("DB_PORT"),
    DB_NAME=os.getenv("DB_NAME")
)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session