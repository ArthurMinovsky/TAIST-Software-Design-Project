import requests
import fastapi

url = 'https://notify-api.line.me/api/notify'
token = '3D9MHq4Sps9Tu4yoFdZTYy7SY2p6h7MEnVcZCUuJlHk'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}


@app.get("/api/route")
def route(num_car):
    if num_car == "0":
        msg = 'กรุณาเข้าจอดในช่อง A'
    if num_car == "1":
        msg = 'กรุณาเข้าจอดในช่อง B'
    if num_car == "2":
        msg = 'กรุณาเข้าจอดในช่อง C'
    if num_car == "3":
        msg = 'กรุณาเข้าจอดในช่อง D'
    r = requests.post(url, headers=headers, data = {'message':msg})
    return "sloting OK"     #200 is OK

db_num = 0

@app.get("/api/displayid")
def displayid(id ,bool(car_status)):
    if car_status == True:
        msg = 'ยินดีต้อนรับคุณเข้าสู่ระบบจอดรถ'
        r = requests.post(url, headers=headers, data = {'RFID':id})
        route(db_num.count())
    if car_status == False:
        msg = 'ขออภัยที่จอดรถเต็มแล้ว'
        r = requests.post(url, headers=headers, data = {'massage':msg})
    return "display OK"     #200 is OK

