import uuid
from typing import Optional
from pydantic import BaseModel, Field


class Car_in(BaseModel):
    car_id: str = Field(...)
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "car_id": "ABC123"
            }
        }

class Car_out(BaseModel):
    car_id: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "car_id": "ABC123"
            }
        }