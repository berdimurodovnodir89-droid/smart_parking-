from sqlalchemy import Column, Integer, String
from app.database.db import Base


class ParkingSlot(Base):
    __tablename__ = "parking_slots"

    id = Column(Integer, primary_key=True, index=True)
    slot_number = Column(Integer, unique=True, nullable=False)
    floor = Column(Integer, default=1)
    status = Column(String, default="free")
