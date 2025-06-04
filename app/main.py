# Path: app/main.py

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from loguru import logger
from contextlib import asynccontextmanager
from app.turso.database import close_db_connections, init_db_alarmas
from app.utils.server_status import log_server_status
from app.server.middlewares import AllowedIPsMiddleware, InvalidRequestLoggingMiddleware, LogResponseMiddleware
from fastapi.middleware.cors import CORSMiddleware

from app.alarms.routes import router as alarms_router
from app.server.routes import router as server_router

#------------------------------------------------------- LOGGING -------------------------------------------------------
logger.add("logs/file_{time:YYYY-MM-DD}.log", rotation="00:00")

#------------------------------------------------------- ASYNC CONTEXT MANAGER -----------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing Alarm databases...")
        
        await init_db_alarmas()   
        logger.info("Databases for Alarm's : OK")
        

        # Iniciar la tarea en segundo plano
        loop = asyncio.get_event_loop()
        loop.create_task(log_server_status())
        #loop.create_task(background_tasks()) 

        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("Shutting down...")
        try:
            await close_db_connections()  # Asegúrate de cerrar las conexiones aquí
        except Exception as e:
            logger.error(f"Error closing database connections: {e}")

#------------------------------------------------------- FASTAPI -------------------------------------------------------
app = FastAPI(lifespan=lifespan)


#------------------------------------------------------- MIDDLEWARE ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Permite solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

# Añadir el middleware de IPs permitidas
app.add_middleware(AllowedIPsMiddleware)

# Añadir el middleware de captura de solicitudes inválidas
app.add_middleware(InvalidRequestLoggingMiddleware)

# Añadir el middleware de log de respuestas
app.add_middleware(LogResponseMiddleware)

#------------------------------------------------------- EXCEPTION HANDLERS ----------------------------------------------
@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    client_ip = request.client.host
    requested_url = str(request.url)
    user_agent = request.headers.get('user-agent', 'unknown')
    logger.warning(f"404 Not Found: {requested_url} from IP: {client_ip} with User-Agent: {user_agent}")
    return JSONResponse(
        status_code=404,
        content={"detail": "Not Found"}
    )

app.include_router(alarms_router, prefix="/alarms", tags=["alarms"])

app.include_router(server_router, prefix="/server", tags=["server"])

