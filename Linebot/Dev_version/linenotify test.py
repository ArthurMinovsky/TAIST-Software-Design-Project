import requests
import fastapi

url = 'https://notify-api.line.me/api/notify'
token = '3D9MHq4Sps9Tu4yoFdZTYy7SY2p6h7MEnVcZCUuJlHk'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
msg = "ยินดีต้อนรับสู่ระบบจอดรถอัจฉริยะ"
r = requests.post(url, headers=headers, data = {'message':msg})
