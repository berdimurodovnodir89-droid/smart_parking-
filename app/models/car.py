from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from app.database.base import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True)
    plate_number = Column(String, unique=True)

    # 🔥 SHU QATORNI QO‘SH
    parking_sessions = relationship("ParkingSession", back_populates="car")
