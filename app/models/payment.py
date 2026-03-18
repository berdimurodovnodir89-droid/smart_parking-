from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime
from datetime import datetime
from app.database.db import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    session_id = Column(Integer, ForeignKey("parking_sessions.id"))
    amount = Column(Float, nullable=False)

    paid_at = Column(DateTime, default=datetime.utcnow)
