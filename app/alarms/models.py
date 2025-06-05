# app/alarms/models.py
# Descripción: SQLAlchemy models para las alarmas en la base de datos de Neon PostgreSQL

from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Alarm(Base):
    __tablename__ = 'tbl_alarms'
    
    id = Column(Integer, primary_key=True, index=True)
    Ticker = Column(String(50), index=True)
    Interval = Column(String(50))
    Quantity = Column(String(50))
    Price_Alert = Column(String(50))    
    Time_Alert = Column(String(50))  # Adjusted to string to match format
    Order = Column(String(50))
    Strategy = Column(String(50))
    raw_data = Column(String(500))
