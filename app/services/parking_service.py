from sqlalchemy.orm import Session
from datetime import datetime

from app.models.car import Car
from app.models.parking_slot import ParkingSlot
from app.models.parking_session import ParkingSession
from app.models.payment import Payment


PRICE_PER_HOUR = 5000


def ensure_slots_exist(db: Session, total_slots: int = 10):
    count = db.query(ParkingSlot).count()

    if count == 0:
        for i in range(1, total_slots + 1):
            slot = ParkingSlot(slot_number=i, floor=1, status="free")
            db.add(slot)
        db.commit()


def get_free_slot(db: Session):
    return db.query(ParkingSlot).filter(ParkingSlot.status == "free").first()


def get_or_create_car(db: Session, plate_number: str):
    car = db.query(Car).filter(Car.plate_number == plate_number).first()

    if not car:
        car = Car(plate_number=plate_number)
        db.add(car)
        db.commit()
        db.refresh(car)

    return car


def start_parking(db: Session, plate_number: str):
    ensure_slots_exist(db)

    car = get_or_create_car(db, plate_number)
    slot = get_free_slot(db)

    if not slot:
        return {"error": "Parking to'lgan"}

    session = ParkingSession(
        car_id=car.id, slot_id=slot.id, entry_time=datetime.utcnow()
    )

    slot.status = "occupied"

    db.add(session)
    db.commit()
    db.refresh(session)

    return {
        "message": "Mashina parkingga kirdi",
        "slot": slot.slot_number,
        "entry_time": session.entry_time,
    }


def end_parking(db: Session, plate_number: str):
    session = (
        db.query(ParkingSession)
        .join(Car)
        .filter(Car.plate_number == plate_number)
        .filter(ParkingSession.status == "active")
        .first()
    )

    if not session:
        return {"error": "Mashina topilmadi"}

    session.exit_time = datetime.utcnow()

    duration = session.exit_time - session.entry_time
    hours = duration.total_seconds() / 3600

    total_price = round(hours * PRICE_PER_HOUR, 2)

    session.total_price = total_price
    session.status = "completed"

    slot = db.query(ParkingSlot).get(session.slot_id)
    slot.status = "free"

    # 🔥 faqat cash payment
    payment = Payment(session_id=session.id, amount=total_price)

    db.add(payment)
    db.commit()

    return {
        "plate_number": plate_number,
        "duration_hours": round(hours, 2),
        "total_price": total_price,
    }
