from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
import math

from app.models.car import Car
from app.models.parking_slot import ParkingSlot
from app.models.parking_session import ParkingSession
from app.models.payment import Payment


PRICE_PER_HOUR = 5000


# ==============================
# SLOTLARNI YARATISH
# ==============================
async def ensure_slots_exist(db: AsyncSession, total_slots: int = 10):
    result = await db.execute(select(ParkingSlot))
    slots = result.scalars().all()

    if not slots:
        for i in range(1, total_slots + 1):
            db.add(ParkingSlot(slot_number=i, floor=1, status="free"))
        await db.commit()


# ==============================
# BO‘SH SLOT OLISH
# ==============================
async def get_free_slot(db: AsyncSession):
    result = await db.execute(select(ParkingSlot).where(ParkingSlot.status == "free"))
    return result.scalars().first()


# ==============================
# CAR TOPISH/YARATISH
# ==============================
async def get_or_create_car(db: AsyncSession, plate_number: str):
    result = await db.execute(select(Car).where(Car.plate_number == plate_number))
    car = result.scalars().first()

    if not car:
        car = Car(plate_number=plate_number)
        db.add(car)
        await db.commit()
        await db.refresh(car)

    return car


# ==============================
# PARKINGGA KIRISH
# ==============================
async def start_parking(db: AsyncSession, plate_number: str):
    await ensure_slots_exist(db)

    car = await get_or_create_car(db, plate_number)
    slot = await get_free_slot(db)

    if not slot:
        return {"error": "Parking to'lgan"}

    session = ParkingSession(
        car_id=car.id,
        slot_id=slot.id,
        entry_time=datetime.utcnow(),
        status="active",  # 🔥 MUHIM
    )

    slot.status = "occupied"

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return {
        "message": "Mashina parkingga kirdi",
        "slot": slot.slot_number,
        "entry_time": session.entry_time,
    }


# ==============================
# PARKINGDAN CHIQISH
# ==============================
async def end_parking(db: AsyncSession, plate_number: str):
    result = await db.execute(
        select(ParkingSession)
        .join(Car)
        .where(Car.plate_number == plate_number)
        .where(ParkingSession.status == "active")
    )
    session = result.scalars().first()

    if not session:
        return {"error": "Mashina topilmadi yoki allaqachon chiqib ketgan"}

    session.exit_time = datetime.utcnow()

    duration = session.exit_time - session.entry_time
    hours = math.ceil(duration.total_seconds() / 3600)  # 🔥 to‘g‘rilangan

    total_price = hours * PRICE_PER_HOUR

    session.total_price = total_price
    session.status = "completed"

    # SLOTNI BO‘SHATISH
    result = await db.execute(
        select(ParkingSlot).where(ParkingSlot.id == session.slot_id)
    )
    slot = result.scalars().first()
    slot.status = "free"

    # PAYMENT
    payment = Payment(session_id=session.id, amount=total_price)

    db.add(payment)
    await db.commit()

    return {
        "plate_number": plate_number,
        "duration_hours": hours,
        "total_price": total_price,
    }


# ==============================
# AKTIV SESSIONLAR
# ==============================
async def get_active_sessions(db: AsyncSession):
    result = await db.execute(
        select(ParkingSession).where(ParkingSession.status == "active")
    )
    sessions = result.scalars().all()

    data = []

    for s in sessions:
        car_result = await db.execute(select(Car).where(Car.id == s.car_id))
        car = car_result.scalars().first()

        data.append(
            {
                "plate_number": car.plate_number,
                "slot_id": s.slot_id,
                "entry_time": s.entry_time,
            }
        )

    return data


# ==============================
# BO‘SH SLOTLAR
# ==============================
async def get_free_slots(db: AsyncSession):
    result = await db.execute(select(ParkingSlot).where(ParkingSlot.status == "free"))
    slots = result.scalars().all()

    return [{"slot_number": s.slot_number, "floor": s.floor} for s in slots]


# ==============================
# DASHBOARD
# ==============================
async def get_dashboard(db: AsyncSession):
    total = await db.execute(select(ParkingSlot))
    total_slots = len(total.scalars().all())

    occupied = await db.execute(
        select(ParkingSlot).where(ParkingSlot.status == "occupied")
    )
    occupied_count = len(occupied.scalars().all())

    free = await db.execute(select(ParkingSlot).where(ParkingSlot.status == "free"))
    free_count = len(free.scalars().all())

    payments = await db.execute(select(Payment))
    payment_list = payments.scalars().all()

    total_income = sum(p.amount for p in payment_list) if payment_list else 0

    return {
        "total_slots": total_slots,
        "occupied": occupied_count,
        "free": free_count,
        "total_income": total_income,
    }
