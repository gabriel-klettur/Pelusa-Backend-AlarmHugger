# Path: app/config.py
import os
from pathlib import Path
from dotenv import load_dotenv
from loguru import logger

# Cargar variables de entorno desde la raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv_path = BASE_DIR / '.env'
logger.info(f"Cargando variables de entorno desde {dotenv_path}")
load_dotenv(dotenv_path)
logger.debug(f"Config loaded: DATABASE_URL={os.getenv('DATABASE_URL')}")

class Settings:
    # Database connection for Neon Postgres
    # Normalize Postgres URL for asyncpg driver
    raw_db_url = os.getenv("DATABASE_URL", "")
    if raw_db_url.startswith("postgres://"):
        DATABASE_URL = raw_db_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif raw_db_url.startswith("postgresql://"):
        DATABASE_URL = raw_db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    else:
        DATABASE_URL = raw_db_url
    # Otros ajustes
    APIURL = os.getenv("APIURL")
    APIKEY = os.getenv("APIKEY")
    SECRETKEY = os.getenv("SECRETKEY")
    ALLOWED_IPS = [ip.strip() for ip in os.getenv("ALLOWED_IPS", "").split(",") if ip.strip()]
    BLOCKED_IPS = os.getenv("BLOCKED_IPS", "").split(",")
    UPLOAD_DIRECTORY = "./app/strateger/uploads/diary"
    MODE_DEVELOPING = os.getenv("MODE_DEVELOPING", "false").strip().lower() in ["true", "1", "yes", "on"]

settings = Settings()
