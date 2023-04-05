import os
import sys
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
from pyngrok import ngrok
from pymongo import MongoClient
from datetime import datetime
from argparse import ArgumentParser

# Define logs
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

# Database code
mongoClient = MongoClient(os.environ['MONGODB_URI'], 27017)
if os.environ["PHASE"] == "DEVELOPMENT":
    app_db = mongoClient.blecollector_test
if os.environ["PHASE"] == "PRODUCTION":
    app_db = mongoClient.blecollector

app = FastAPI()

channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    logging.error('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    logging.error('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
count = 0

@app.get("/", response_class=HTMLResponse)
def hello_world():
    return "Hello, World!"

@app.get("/api")
def api_func(userId: str) -> dict:
    user_col = app_db.user # Collection
    ans = user_col.find_one({"userId": userId})
    logging_col = app_db.logging # Collection
    ans = logging_col.find_one({"ble": ans['ble']})
    location_col = app_db.location # Collection
    ans = location_col.find_one({"detector_id": ans['detector_id']})
    resp = {"userId": userId, "place":ans['place']}
    return resp

@app.post("/api/inject_user")
async def inject_user(request: Request):
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = await request.json()
        data['timestamp'] = datetime.now()
        user_col = app_db.user
        user_col.insert_one(data)
        return {"status": "OK"}
    return {"status": "ERROR"}

@app.post("/api/inject_logging")
async def inject_logging(request: Request):
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = await request.json()
        data['timestamp'] = datetime.now()
        logging_col = app_db.logging
        logging_col.insert_one(data)
        return {"status": "OK"}
    return {"status": "ERROR"}

@app.post("/api/inject_location")
async def inject_location(request: Request):
    if os.environ["PHASE"] == "DEVELOPMENT":
        data = await request.json()
        data['timestamp'] = datetime.now()
        location_col = app_db.location
        location_col.insert_one(data)
        return {"status": "OK"}
    return {"status": "ERROR"}

@app.get("/api/query_user")
def query_user(userId: str) -> dict:
    if os.environ["PHASE"] == "DEVELOPMENT":
        user_col = app_db.user
        ans = user_col.find_one({"userId": userId})
        resp = {"userId": userId, "ble": ans["ble"]}
        return resp
    return {"status": "ERROR"}

@app.post("/callback")
async def callback(request: Request):
    signature = request.headers['X-Line-Signature']
    body = await request.body()
    logging.info("Request body: " + body.decode())

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        return {"code": "400", "message": "Invalid signature error"}

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text + ', me too')
    )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()
    ngrok.set_auth_token(os.environ['NGROK_TOKEN'])
    public_url = ngrok.connect(options.port)
    url = public_url.public_url.replace('http', 'https') + '/callback'
    print(url)
    line_bot_api.set_webhook_endpoint(url)
    app.run(debug=options.debug, port=options.port, host='0.0.0.0', use_reloader=False)