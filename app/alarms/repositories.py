# Path: app/alarms/crud.py

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.alarms.models import Alarm

async def save_alarm(db: AsyncSession, variables: dict, raw_data: str):
    db_alarm = Alarm(
        Ticker=variables.get('Ticker'),
        Temporalidad=variables.get('Temporalidad'),
        Quantity=variables.get('Quantity'),
        Entry_Price_Alert=variables.get('Entry_Price_Alert'),
        Exit_Price_Alert=variables.get('Exit_Price_Alert'),
        Time_Alert=variables.get('Time_Alert'),
        Order=variables.get('Order'),
        Strategy=variables.get('Strategy'),
        raw_data=raw_data
    )
    db.add(db_alarm)
    await db.commit()
    await db.refresh(db_alarm)
    return db_alarm

async def get_alarms(db: AsyncSession, limit: int = 10, offset: int = 0, latest: bool = False):
    query = select(Alarm).offset(offset).limit(limit)
    if latest:
        query = query.order_by(Alarm.id.desc())
    result = await db.execute(query)
    return result.scalars().all()

async def get_latest_alarm_with_entry(db: AsyncSession, strategy_name: str, ticker: str, entry_order: str, temporalidad: str):
    result = await db.execute(
        select(Alarm)
        .where(Alarm.Strategy == strategy_name)
        .where(Alarm.Ticker == ticker)
        .where(Alarm.Order == entry_order)
        .where(Alarm.Temporalidad == temporalidad)
        .order_by(Alarm.id.desc())
        .limit(1)
    )
    return result.scalars().first()
