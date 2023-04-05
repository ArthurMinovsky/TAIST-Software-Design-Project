import requests
from fastapi import FastAPI

url = 'https://notify-api.line.me/api/notify'
token = '3D9MHq4Sps9Tu4yoFdZTYy7SY2p6h7MEnVcZCUuJlHk'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

app = FastAPI()

@app.get("/api/route")
def route(num_car):
    if num_car == "0":
        msg = 'Your Stall ID is A'
    if num_car == "1":
        msg = 'Your Stall ID is B'
    if num_car == "2":
        msg = 'Your Stall ID is C'
    if num_car == "3":
        msg = 'Your Stall ID is D'
    r = requests.post(url, headers=headers, data = {'message':msg})
    return "sloting OK"     #200 is OK

db_num = 0

@app.get("/api/displayid")
def displayid(id ,bool(car_status)):
    if car_status == True:
        msg = 'Welcome to our parking lot system' 
        r = requests.post(url, headers=headers, data = {'RFID':id})
        route(db_num.count())
    if car_status == False:
        msg = 'Sorry, we have run out of parking stalls'
        r = requests.post(url, headers=headers, data = {'massage':msg})
    return "display OK"     #200 is OK

# uvicorn 
