# Path: app/alarms/routes.py

from fastapi import APIRouter, Depends, HTTPException, Request, Query       #FastAPI           
from sqlalchemy.ext.asyncio import AsyncSession                             #Base de datos        
from app.db.database import get_db                          #Base de datos

from app.alarms.schemas import AlarmCreate, AlarmResponse                   #Schemas   
from app.alarms.repositories import save_alarm                            #Base de datos

from app.utils.ip_check import is_ip_allowed                                #Seguridad
from app.alarms.utils import convierte_temporalidad                         #Utilidades

from loguru import logger                                                   #Logging
from typing import List                                                     #Tipado         

from datetime import datetime                                               #Fecha y hora

router = APIRouter()

"""
    Handle incoming webhook requests to create and process alarms.
    Args:
        request (Request): The incoming HTTP request.
        alarm_data (AlarmCreate): The alarm data received in the request body.
        db_alarmas (AsyncSession): Database session for alarm operations.
        db_estrategias (AsyncSession): Database session for strategy operations.
    Returns:
        AlarmResponse: The response model containing the saved alarm details.
    Raises:
        HTTPException: If the IP is not allowed or any other error occurs during processing.
"""
@router.post("/webhook", response_model=AlarmResponse)
async def webhook(request: Request, alarm_data: AlarmCreate, db_alarmas: AsyncSession = Depends(get_db)):
    try:
        client_ip = request.client.host
        #logger.info(f"Alarm received from {client_ip}")
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{current_time}]-AlarmHugger - Alarm received from {client_ip}")
        

        # Verificar si la IP está permitida
        await is_ip_allowed(client_ip)

        #logger.debug(f"Alarm Data: {alarm_data.json()}")

        variables = alarm_data.dict()
        
        # Convertir la temporalidad
        variables['Interval'] = convierte_temporalidad(variables.get('Interval'))
        
        raw_data = alarm_data.json()

        saved_alarm = await save_alarm(db_alarmas, variables, raw_data)
        logger.info(f"Alarm saved in DB, with Id: {saved_alarm.id}")

        return AlarmResponse.from_orm(saved_alarm)
    except HTTPException:
        raise  # Re-lanzar la excepción HTTP
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing the alarm")
