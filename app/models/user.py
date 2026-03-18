from sqlalchemy import Column, Integer, String
from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    phone = Column(String)
    role = Column(String, default="operator")
