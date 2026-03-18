from app.services.parking_service import (
    get_active_sessions,
    get_free_slots,
    get_dashboard,
)
from app.database.db import SessionLocal

db = SessionLocal()

from app.models.parking_session import ParkingSession
from app.models.parking_slot import ParkingSlot


print("ACTIVE:", get_active_sessions(db))
print("FREE:", get_free_slots(db))
print("DASHBOARD:", get_dashboard(db))
