# Path: app/db/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from loguru import logger
from app.db.base import Base

raw_db_url = settings.DATABASE_URL
# Remove sslmode from URL and configure SSL for asyncpg
parts = raw_db_url.split("?", 1)
db_url = parts[0]
query_part = parts[1] if len(parts) > 1 else ""
connect_args = {"ssl": True} if "sslmode=require" in query_part else {}
engine = create_async_engine(
    db_url,
    connect_args=connect_args,
    pool_recycle=3600,
    pool_pre_ping=True
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

async def get_db():
    async with SessionLocal() as db:
        yield db

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def close_db():
    await engine.dispose()
