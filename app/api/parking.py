from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_db
from app.schemas.parking import ParkingEnterRequest, ParkingExitRequest
from app.services.parking_service import (
    start_parking,
    end_parking,
    get_active_sessions,
    get_free_slots,
    get_dashboard,
)

router = APIRouter(prefix="/parking", tags=["Parking"])


@router.post("/enter", status_code=201)
async def enter_parking(data: ParkingEnterRequest, db: AsyncSession = Depends(get_db)):
    return await start_parking(db, data.plate_number)


@router.post("/exit")
async def exit_parking(data: ParkingExitRequest, db: AsyncSession = Depends(get_db)):
    return await end_parking(db, data.plate_number)


@router.get("/active")
async def active(db: AsyncSession = Depends(get_db)):
    return await get_active_sessions(db)


@router.get("/free-slots")
async def free_slots(db: AsyncSession = Depends(get_db)):
    return await get_free_slots(db)


@router.get("/dashboard")
async def dashboard(db: AsyncSession = Depends(get_db)):
    return await get_dashboard(db)
