# Path: app/config.py
import os
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

class Settings:
    # Toggle Turso usage: set USE_TURSO=true in .env for production
    USE_TURSO = os.getenv("USE_TURSO", "false").lower() in ["true", "1", "yes", "on"]
    # Local SQLite paths
    SQLITE_DIR = os.getenv("SQLITE_DIR", "./data_sqlite")
    DATABASE_URL_DESARROLLO_ALARMAS     = f"sqlite+aiosqlite:///{SQLITE_DIR}/alarms.sqlite"
    DATABASE_URL_DESARROLLO_ESTRATEGIAS = f"sqlite+aiosqlite:///{SQLITE_DIR}/estrategias.sqlite"
    DATABASE_URL_DESARROLLO_DIARY       = f"sqlite+aiosqlite:///{SQLITE_DIR}/diary.sqlite"
    DATABASE_URL_DESARROLLO_POSITIONS   = f"sqlite+aiosqlite:///{SQLITE_DIR}/positions.sqlite"
    DATABASE_URL_DESARROLLO_ACCOUNTS    = f"sqlite+aiosqlite:///{SQLITE_DIR}/accounts.sqlite"
    DATABASE_URL_DESARROLLO_KLINE_DATA  = f"sqlite+aiosqlite:///{SQLITE_DIR}/kline_data.sqlite"
    DATABASE_URL_DESARROLLO_ORDERS      = f"sqlite+aiosqlite:///{SQLITE_DIR}/orders.sqlite"
    # Turso (production URLs)
    DATABASE_URL_PROD_ALARMAS     = os.getenv("TURSO_URL_ALARMAS", "")
    DATABASE_URL_PROD_ESTRATEGIAS = os.getenv("TURSO_URL_ESTRATEGIAS", "")
    DATABASE_URL_PROD_DIARY       = os.getenv("TURSO_URL_DIARY", "")
    DATABASE_URL_PROD_POSITIONS   = os.getenv("TURSO_URL_POSITIONS", "")
    DATABASE_URL_PROD_ACCOUNTS    = os.getenv("TURSO_URL_ACCOUNTS", "")
    DATABASE_URL_PROD_KLINE_DATA  = os.getenv("TURSO_URL_KLINE_DATA", "")
    DATABASE_URL_PROD_ORDERS      = os.getenv("TURSO_URL_ORDERS", "")

    @property
    def DATABASE_URL_ALARMAS(self):
        return self.DATABASE_URL_PROD_ALARMAS if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_ALARMAS

    @property
    def DATABASE_URL_ESTRATEGIAS(self):
        return self.DATABASE_URL_PROD_ESTRATEGIAS if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_ESTRATEGIAS

    @property
    def DATABASE_URL_DIARY(self):
        return self.DATABASE_URL_PROD_DIARY if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_DIARY

    @property
    def DATABASE_URL_POSITIONS(self):
        return self.DATABASE_URL_PROD_POSITIONS if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_POSITIONS

    @property
    def DATABASE_URL_ACCOUNTS(self):
        return self.DATABASE_URL_PROD_ACCOUNTS if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_ACCOUNTS

    @property
    def DATABASE_URL_KLINE_DATA(self):
        return self.DATABASE_URL_PROD_KLINE_DATA if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_KLINE_DATA

    @property
    def DATABASE_URL_ORDERS(self):
        return self.DATABASE_URL_PROD_ORDERS if self.USE_TURSO else self.DATABASE_URL_DESARROLLO_ORDERS

    # Otros ajustes
    APIURL = os.getenv("APIURL")
    APIKEY = os.getenv("APIKEY")
    SECRETKEY = os.getenv("SECRETKEY")
    ALLOWED_IPS = [ip.strip() for ip in os.getenv("ALLOWED_IPS", "").split(",") if ip.strip()]
    BLOCKED_IPS = os.getenv("BLOCKED_IPS", "").split(",")
    UPLOAD_DIRECTORY = "./app/strateger/uploads/diary"
    MODE_DEVELOPING = os.getenv("MODE_DEVELOPING", "false").strip().lower() in ["true", "1", "yes", "on"]

settings = Settings()
