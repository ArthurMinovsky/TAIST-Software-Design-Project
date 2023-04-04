from fastapi import (APIRouter, Body, Request, Response, HTTPException, status, FastAPI)
from fastapi.encoders import jsonable_encoder
import datetime
import pymongo
import math

from pymongo import MongoClient
from dotenv import dotenv_values

from models import  Car_in, Car_out

config = dotenv_values(".env")

app = FastAPI()

mongodb_client = MongoClient(config["ATLAS_URI"])
db = mongodb_client[config["CAR_PARKING_DB"]]


def calculate_fee(time_in:str,time_out:str):
    time_in = time_in[11:]
    time_out = time_out[11:]
    print(time_in,time_out)
    time_in = datetime.datetime.strptime(time_in, '%H:%M:%S').time()
    time_out = datetime.datetime.strptime(time_out, '%H:%M:%S').time()
    time_diff = (datetime.datetime.combine(datetime.date.today(), time_out) - datetime.datetime.combine(datetime.date.today(), time_in))
    print(time_diff)
    hour = time_diff.total_seconds() / 3600
    if hour <= 0.25:
        fee = 0
    elif hour > 0.25 and hour < 1:
        fee = 20
    else:
        fee = math.ceil(hour) * 20
    return fee

@app.on_event("startup")
def startup_db_client():
    print("Connected to the MongoDB database!")
    print(f"link: {config['ATLAS_URI']}")
    print(db.list_collection_names())

@app.get("/")
async def root():
    return {"message": "Welcome to Car parking API!"}

@app.get("/parking")
async def get_parking_status():
    parking_data = db[config["PARKING"]].find()
    parking_data = [i for i in parking_data]
    parking_dict = {i["stall_id"]:{i["stall_status"],
                                   i["car_id"]} 
                                   for i in parking_data}
    return parking_dict

@app.get("/get_car_in")
async def get_car_in():
    car_in_data = db[config["CAR_IN"]].find()
    car_in_data = [i for i in car_in_data]
    car_in_dict = {i["car_id"]:i["time_in"] for i in car_in_data}
    return car_in_dict

@app.get("/get_car_out")
async def get_car_out():
    car_out_data = db[config["CAR_OUT"]].find()
    car_out_data = [i for i in car_out_data]
    car_out_dict = {i["car_id"]:{i["time_out"],
                                i["fee"],
                                i["stall_id"]} 
                    for i in car_out_data}
    return car_out_dict

@app.post("/add_car_in", response_description="Car in")
def car_in(car_in: Car_in):
    car_in = jsonable_encoder(car_in)
    # check if parking is full
    if not db[config["PARKING"]].find_one({"stall_status":0}):
        raise HTTPException(status_code=400, detail="Parking is full")

    elif not db[config["PARKING"]].find_one({"car_id":car_in["car_id"]}):
        assign_parking = db[config["PARKING"]].find_one({"stall_status":0})
        car_in_insert_data = { 
            "time_in":car_in["time_in"],
            "stall_id":assign_parking["stall_id"],
            "car_id":car_in["car_id"]
            }
        parking_update_data = {
            "stall_status":1,
            "car_id":car_in["car_id"]
            }
        db[config["CAR_IN"]].insert_one(car_in_insert_data)
        db[config["PARKING"]].update_one(
            {"stall_id":assign_parking["stall_id"]},
            {"$set":parking_update_data})
        
        return {"message": f"Car : {car_in} inserted into {assign_parking['stall_id']}"}
    
    else :
        raise HTTPException(status_code=400, detail="Car already in the parking")
    

@app.post("/add_car_out", response_description="Car out")
def car_out(car_out: Car_out):
    car_out = jsonable_encoder(car_out)
    # check if car is in the parking
    print(car_out["car_id"])
    print(db[config["PARKING"]].find_one({"car_id":car_out["car_id"]}))
    if not db[config["PARKING"]].find_one({"car_id":car_out["car_id"]}):
        raise HTTPException(status_code=400, detail="Car not in the parking")
    else:
        # get the stall id
        car_in_data = db[config["CAR_IN"]].find_one({"car_id":car_out["car_id"]})
        time_in = car_in_data["time_in"]
        time_out = car_out["time_out"]

        fee = calculate_fee(time_in,time_out)

        stall_id = car_in_data["stall_id"]
        print(stall_id)
        car_out_insert_data = {
            "car_id":car_out["car_id"],
            "time_in":car_in_data["time_in"],
            "time_out":car_out["time_out"],
            
            "stall_id":stall_id,
            "fee":fee
            }
        parking_update_data = {
            "stall_status":0,
            "car_id":None
            }
        db[config["CAR_OUT"]].insert_one(car_out_insert_data)
        db[config["PARKING"]].update_one(
            {"stall_id":stall_id},
            {"$set":parking_update_data})
        return {"message": f"Car : {car_out} removed from {stall_id}"}


@app.on_event("shutdown")
def shutdown_db_client():
    mongodb_client.close()
    print("MongoDB connection closed.")