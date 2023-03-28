from typing import Optional
from fastapi import FastAPI, Request, Response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = FastAPI()

# Replace with your LINE Channel Access Token and Channel Secret
CHANNEL_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# Replace with your LIFF URL
LIFF_URL = "YOUR_LIFF_URL"

# Get massage from user with rich menu
@app.post("/get massage")
async def get_massage(request: Request, response: Response):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        response.status_code = 400
        return "Invalid signature"
    return "OK"

@app.post("/webhook")
async def webhook(request: Request, response: Response):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        response.status_code = 400
        return "Invalid signature"
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text = event.message.text
    reply_token = event.reply_token
    if text == "liff":
        message = TextSendMessage(text=LIFF_URL)
        line_bot_api.reply_message(reply_token, message)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
