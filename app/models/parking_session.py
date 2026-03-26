from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from datetime import datetime
from app.database.base import Base
from sqlalchemy.orm import relationship


class ParkingSession(Base):
    __tablename__ = "parking_sessions"

    id = Column(Integer, primary_key=True, index=True)

    car_id = Column(Integer, ForeignKey("cars.id"))
    slot_id = Column(Integer, ForeignKey("parking_slots.id"))

    entry_time = Column(DateTime, default=datetime.utcnow)
    exit_time = Column(DateTime, nullable=True)

    total_price = Column(Float, nullable=True)

    status = Column(String, default="active")

    car = relationship("Car", back_populates="parking_sessions")
    slot = relationship("ParkingSlot", back_populates="parking_sessions")
