from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Parking_Update, Car_in, Car_out

router = APIRouter()

@router.get("/parking", response_description="Parking retrieved")
def get_parking(request: Request):
    parking = request.app.parking_db["parking"]
    parking = parking.find()
    return list(parking)

@router.post("/car_in", response_description="Car in")
def car_in(car_in: Car_in, request: Request):
    car_in = jsonable_encoder(car_in)
    car_in = request.app.car_db["car_in"].insert_one(car_in)
    return car_in
  
@router.post("/car_out", response_description="Car out")
def car_out(car_out: Car_out, request: Request):
    car_out = jsonable_encoder(car_out)
    car_out = request.app.car_db["car_out"].insert_one(car_out)
    return car_out
  
@router.post("/parking_update", response_description="Parking updated")
def parking_update(parking_update: Parking_Update, request: Request):
    parking_update = jsonable_encoder(parking_update)
    parking_update = request.app.parking_db["parking_update"].insert_one(parking_update)
    return parking_update