from fastapi import FastAPI
import pymongo
from pymongo import MongoClient
from dotenv import dotenv_values
from route import router

config = dotenv_values(".env")
# connect to MongoDB.

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])

    app.car_in_db = app.mongodb_client[config["CAR_IN_DB"]]
    app.car_out_db = app.mongodb_client[config["CAR_OUT_DB"]]
    app.parking_db = app.mongodb_client[config["PARKING_DB"]]
    print("Connected to the MongoDB database!")

@app.get("/")
async def root():
    return {"message": "Welcome to the PyMongo tutorial!"}

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(router)

# uvicorn api.main:app --reload --port 8000