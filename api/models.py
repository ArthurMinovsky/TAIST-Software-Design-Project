import uuid
from typing import Optional
from pydantic import BaseModel, Field

class Parking_Update(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    Stall_ID: str = Field(...)
    Time: str = Field(...)
    Status: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "Stall_ID": "A1",
                "Time": "2021-05-01 12:00:00",
                "Status": "Available",
            }
        }

class Car_in(BaseModel):
    id : str = Field(default_factory=uuid.uuid4, alias="_id")
    car: str = Field(...)
    time: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "car": "ABC123",
                "time": "2021-05-01 12:00:00",
            }
        }

class Car_out(BaseModel):
    id : str = Field(default_factory=uuid.uuid4, alias="_id")
    car: str = Field(...)
    time: str = Field(...)
    stall: str = Field(...)
    fee: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "car": "ABC123",
                "time": "2021-05-01 12:00:00",
                "stall": "A1",
                "fee": "50",
            }
        }