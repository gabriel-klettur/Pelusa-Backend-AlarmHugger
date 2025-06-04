# Path: app/turso/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.config import settings
from loguru import logger
from app.turso.base import BaseAlarmas

# Configuración de la base de datos (Turso vs SQLite local)
connect_args = {"auth_token": settings.TURSO_AUTH_TOKEN} if settings.USE_TURSO else {"check_same_thread": False}
engine_alarmas = create_async_engine(
    settings.DATABASE_URL_ALARMAS,
    connect_args=connect_args,
    pool_recycle=3600,
    pool_pre_ping=True
)
SessionLocalAlarmas = sessionmaker(autocommit=False, autoflush=False, bind=engine_alarmas, class_=AsyncSession)

async def get_db_alarmas():
    async with SessionLocalAlarmas() as db:
        yield db

async def init_db_alarmas():
    async with engine_alarmas.begin() as conn:
        await conn.run_sync(BaseAlarmas.metadata.create_all)

async def close_db_connections():
    await engine_alarmas.dispose()
