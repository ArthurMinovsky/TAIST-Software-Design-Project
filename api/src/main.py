from fastapi import (APIRouter, Body, Request, Response, HTTPException, status, FastAPI)
from fastapi.encoders import jsonable_encoder
import datetime
import pymongo
import math
import pandas as pd
import requests

from pymongo import MongoClient
from dotenv import dotenv_values

from .models import  Car_in, Car_out

RFID_TO_CAR_ID = {}

line_url = 'https://notify-api.line.me/api/notify'
line_token = '3D9MHq4Sps9Tu4yoFdZTYy7SY2p6h7MEnVcZCUuJlHk'
line_headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+line_token}

config = dotenv_values(".env")

app = FastAPI()

mongodb_client = MongoClient(config["ATLAS_URI"])
db = mongodb_client[config["CAR_PARKING_DB"]]

def calculate_fee(time_in:str,time_out:str):
    time_in = time_in[11:]
    time_out = time_out[11:]
    time_in = datetime.datetime.strptime(time_in, '%H:%M:%S').time()
    time_out = datetime.datetime.strptime(time_out, '%H:%M:%S').time()
    time_diff = (datetime.datetime.combine(datetime.date.today(), time_out) - datetime.datetime.combine(datetime.date.today(), time_in))
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
    
    dblist = mongodb_client.list_database_names()
    if "parking_db" in dblist:
        print("The database exists.")
    else:
        print("The database does not exist.")
        print("The database and collections is now being created...")
        db = mongodb_client["parking_db"]
        car_in = db[config['CAR_IN']]
        car_out = db[config['CAR_OUT']]
        parking = db[config['PARKING']]
        parking_list = ["A","B","C","D"]
        for i in parking_list:
            parking.insert_one(
                {
                    "stall_id":i,
                    "stall_status":0,
                    "car_id":None}
                )
    print("The database and collections have been created.")

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
    # get current time as YYYY-MM-DD HH:MM:SS
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # check if parking is full
    if not db[config["PARKING"]].find_one({"stall_status":0}):

        message = "Parking is full"
        requests.post(line_url, headers=line_headers, data = {'message':message})
        
        raise HTTPException(status_code=400, detail="Parking is full")

    elif not db[config["PARKING"]].find_one({"car_id":car_in["car_id"]}):
        assign_parking = db[config["PARKING"]].find_one({"stall_status":0})
        car_in_insert_data = { 
            "time_in":current_time,
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
        message = f"Car : {car_in} inserted into {assign_parking['stall_id']}"
        
        requests.post(line_url, headers=line_headers, data = {'message':message})

        return {"message": f"Car : {car_in} inserted into {assign_parking['stall_id']}"}
    
    else :
        raise HTTPException(status_code=400, detail="Car already in the parking")
    

@app.post("/add_car_out", response_description="Car out")
def car_out(car_out: Car_out):
    car_out = jsonable_encoder(car_out)
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # check if car is in the parking
    print(car_out["car_id"])
    print(db[config["PARKING"]].find_one({"car_id":car_out["car_id"]}))
    if not db[config["PARKING"]].find_one({"car_id":car_out["car_id"]}):
        raise HTTPException(status_code=400, detail="Car not in the parking")
    else:
        # get the stall id
        car_in_data = db[config["CAR_IN"]].find_one({"car_id":car_out["car_id"]})
        time_in = car_in_data["time_in"]
        time_out = current_time

        fee = calculate_fee(time_in,time_out)

        stall_id = car_in_data["stall_id"]
        car_out_insert_data = {
            "car_id":car_out["car_id"],
            "time_in":car_in_data["time_in"],
            "time_out":current_time,
            
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
        
        message = f"Car : {car_out} removed from {stall_id} | fee : {fee}"
        requests.post(line_url, headers=line_headers, data = {'message':message})
        return {"message": f"Car : {car_out} removed from {stall_id}"}

@app.get("/monthly_total_fee")
def get_total_fee():
    car_out = db[config["CAR_OUT"]]
    car_out_data = [i for i in car_out.find()]
    car_out_df = pd.DataFrame(car_out_data)
    car_out_df["time_out"] = pd.to_datetime(car_out_df["time_out"])
    car_out_df["month"] = car_out_df["time_out"].dt.month
    monthly_fee_df = car_out_df[['month','fee']].groupby('month').sum()
    return monthly_fee_df.to_dict()

@app.get("/get_latest_fee/{car_id}")
def get_latest_fee(car_id):
    car_out = db[config["CAR_OUT"]]
    sorted_car_out = car_out.find({"car_id":car_id}).sort("time_out",-1)
    latest_data = list(sorted_car_out)[0]
    fee = latest_data["fee"]
    return {"car_id":car_id,"fee":fee}

# @app.get("/welcome_car/{car_id}")
# def get_stall_from_car(car_id):
#     parking_of_car = db[config["PARKING"]].find_one({"car_id":car_id})
#     if parking_of_car:
#         message = f"Car {car_id} is in stall {parking_of_car['stall_id']}"
#         requests.post(line_url,headers=line_headers,data={"message":message})
#         return {"car_id":car_id,"stall_id":parking_of_car["stall_id"]}
#     else:
#         raise HTTPException(status_code=400, detail="Car not in the parking")

@app.get("/welcome_car/{car_id}")
def check_full_parking():
    empty_parking_count = db[config["PARKING"]]\
        .find({"stall_status":0})\
        .count()
    return empty_parking_count == 0


@app.on_event("shutdown")
def shutdown_db_client():
    mongodb_client.close()
    print("MongoDB connection closed.")