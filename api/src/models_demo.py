import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Car_in(BaseModel):
    car_id: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "car_id": "ABC123",
                "time_in": "2021-05-01 12:00:00",
            }
        }

class Car_out(BaseModel):
    car_id: str = Field(...)
    time_out: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "car_id": "ABC123",
                "time_out": "2021-05-01 13:00:00"
            }
        }