from pydantic import BaseModel


class ParkingEnterRequest(BaseModel):
    plate_number: str


class ParkingExitRequest(BaseModel):
    plate_number: str
