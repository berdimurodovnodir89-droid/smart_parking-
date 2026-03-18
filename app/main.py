from fastapi import FastAPI
from app.api.parking import router as parking_router

app = FastAPI()

app.include_router(parking_router)


@app.get("/")
async def root():
    return {"message": "Ishlayapti 🚀"}


from app.database.base import Base
from app.database.db import engine

# MODELLARNI IMPORT QILISH SHART
from app.models import car, parking_slot, parking_session, payment


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
