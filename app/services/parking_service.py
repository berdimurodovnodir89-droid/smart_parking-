from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from datetime import datetime, date

import math

from app.models.car import Car
from app.models.parking_slot import ParkingSlot
from app.models.parking_session import ParkingSession
from app.models.payment import Payment

PRICE_PER_HOUR = 5000


# ==============================
# SLOT INIT
# ==============================
async def ensure_slots_exist(db: AsyncSession, total_slots: int = 10):
    result = await db.execute(select(ParkingSlot))
    slots = result.scalars().all()

    if not slots:
        for i in range(1, total_slots + 1):
            db.add(ParkingSlot(slot_number=i, floor=1, status="free"))
        await db.commit()


# ==============================
# FREE SLOT (TARTIBLI)
# ==============================
async def get_free_slot(db: AsyncSession):
    result = await db.execute(
        select(ParkingSlot).where(ParkingSlot.status == "free").order_by(ParkingSlot.id)
    )
    return result.scalars().first()


# ==============================
# CAR
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
# ENTER (VALIDATION BOR)
# ==============================
async def start_parking(db: AsyncSession, plate_number: str):
    await ensure_slots_exist(db)

    car = await get_or_create_car(db, plate_number)

    # ❗ CHECK: mashina ichkaridami
    existing = await db.execute(
        select(ParkingSession).where(
            ParkingSession.car_id == car.id, ParkingSession.status == "active"
        )
    )

    if existing.scalars().first():
        return {"error": "Mashina allaqachon parkingda"}

    slot = await get_free_slot(db)

    if not slot:
        return {"error": "Parking to'lgan"}

    session = ParkingSession(
        car_id=car.id,
        slot_id=slot.id,
        entry_time=datetime.utcnow(),
        status="active",
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
# EXIT (VALIDATION BOR)
# ==============================
async def end_parking(db: AsyncSession, plate_number: str):
    result = await db.execute(
        select(ParkingSession)
        .options(selectinload(ParkingSession.car), selectinload(ParkingSession.slot))
        .join(Car)
        .where(Car.plate_number == plate_number)
        .where(ParkingSession.status == "active")
    )

    session = result.scalars().first()

    if not session:
        return {"error": "Mashina parkingda emas yoki chiqib bo‘lgan"}

    session.exit_time = datetime.utcnow()

    duration = session.exit_time - session.entry_time
    hours = math.ceil(duration.total_seconds() / 3600)

    total_price = hours * PRICE_PER_HOUR

    session.total_price = total_price
    session.status = "completed"

    # SLOT BO‘SHATISH
    session.slot.status = "free"

    payment = Payment(session_id=session.id, amount=total_price)

    db.add(payment)
    await db.commit()

    return {
        "plate_number": plate_number,
        "duration_hours": hours,
        "total_price": total_price,
    }


# ==============================
# ACTIVE (OPTIMIZED)
# ==============================
async def get_active_sessions(db: AsyncSession):
    result = await db.execute(
        select(ParkingSession)
        .options(selectinload(ParkingSession.car), selectinload(ParkingSession.slot))
        .where(ParkingSession.status == "active")
    )

    sessions = result.scalars().all()

    return [
        {
            "plate_number": s.car.plate_number,
            "slot": s.slot.slot_number,
            "entry_time": s.entry_time,
        }
        for s in sessions
    ]


# ==============================
# FREE SLOTS (TARTIBLI)
# ==============================
async def get_free_slots(db: AsyncSession):
    result = await db.execute(
        select(ParkingSlot).where(ParkingSlot.status == "free").order_by(ParkingSlot.id)
    )

    slots = result.scalars().all()

    return [{"slot_number": s.slot_number, "floor": s.floor} for s in slots]


# ==============================
# DASHBOARD
# ==============================

from datetime import datetime, date
from sqlalchemy import select, func

from datetime import datetime, date, timedelta
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.parking_slot import ParkingSlot
from app.models.payment import Payment


async def get_dashboard(db: AsyncSession):
    # ===== SLOTLAR =====
    total = await db.execute(select(ParkingSlot))
    total_slots = len(total.scalars().all())

    occupied = await db.execute(
        select(ParkingSlot).where(ParkingSlot.status == "occupied")
    )
    occupied_count = len(occupied.scalars().all())

    free = await db.execute(select(ParkingSlot).where(ParkingSlot.status == "free"))
    free_count = len(free.scalars().all())

    # ===== BUGUNGI VAQT ORALIG‘I =====
    today = date.today()
    start = datetime.combine(today, datetime.min.time())  # 00:00
    end = start + timedelta(days=1)  # ertaga 00:00

    # ===== FAQAT BUGUNGI DAROMAD =====
    result = await db.execute(
        select(func.sum(Payment.amount))
        .where(Payment.paid_at >= start)
        .where(Payment.paid_at < end)
    )

    today_income = result.scalar()

    if today_income is None:
        today_income = 0

    return {
        "total_slots": total_slots,
        "occupied": occupied_count,
        "free": free_count,
        "today_income": today_income,
    }
