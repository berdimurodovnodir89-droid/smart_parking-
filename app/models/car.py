from sqlalchemy import Column, Integer, String

from app.database.base import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    plate_number = Column(String, unique=True, nullable=False)
    model = Column(String)
    color = Column(String)
