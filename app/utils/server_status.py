# app/utils/server_status.py

import asyncio
from loguru import logger

async def log_server_status():
    while True:
        try:            
            logger.info("AlarmHugger - Server is running smoothly")
        except Exception as e:
            logger.error(f"AlarmHugger - Server status check failed: {e}")
        await asyncio.sleep(60) 
