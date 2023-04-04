from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

from models import Parking_Update, Car_in, Car_out

router = APIRouter()

def update_parking(parking_db,stall_id, stall_status):

    parking_list = parking_db.find()
    assert stall_status in [0,1], "stall_status must be 0 or 1"
    assert stall_id in [i["stall_id"] for i in parking_list], f"{stall_id} not found"

    parking_db.update_one(
        {"stall_id":stall_id},
        {"$set":{"stall_status":stall_status}}
    )
    return f"{stall_id} updated"

@router.post("/car_in", response_description="Car in")
def car_in(car_in: Car_in, request: Request):
    car_in = jsonable_encoder(car_in)
    car_in_res = request.app.car_db["car_in"].insert_one(car_in)
    update_parking(request.app.parking_db,car_in["stall_id"],1)
    return car_in_res

@router.post("/car_out", response_description="Car out")
def car_out(car_out: Car_out, request: Request):
    car_out = jsonable_encoder(car_out)
    car_out_res = request.app.car_db["car_out"].insert_one(car_out)
    update_parking(request.app.parking_db,car_out["stall_id"],0)
    return car_out_res

@router.get("/parking", response_description="Parking retrieved")
def get_parking_status(request: Request):
    parking_list = request.app.parking_db.find()
    return parking_list
