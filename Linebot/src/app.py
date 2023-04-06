from fastapi import FastAPI, Request, Response
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = FastAPI()

# Channel access token and channel secret
line_bot_api = LineBotApi(os.environ.get('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('LINE_CHANNEL_SECRET'))



# Replace with your LIFF URL
LIFF_URL = "https://liff.line.me/1660815308-xpr8JBGb"

# Get massage from user with rich menu
@app.get("/get massage")
async def get_massage(request: Request, response: Response):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        response.status_code = 400
        return "Invalid signature"
    return "OK"

# Reply massage to user
@app.post("/line/webhook")
async def line_webhook(request: Request, response: Response):
    # Get request body and signature
    body = await request.body()
    signature = request.headers['X-Line-Signature']

    # Handle webhook event
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        response.status_code = 400
        return "Invalid signature"

    # Return success response
    return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text = event.message.text
    reply_token = event.reply_token
    if text == "liff":
        message = TextSendMessage(text=LIFF_URL)
        line_bot_api.reply_message(reply_token, message)

# Handler for Line message event
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

# Endpoint for LIFF app
@app.get("/liff")
async def liff():
    # Return LIFF app content
    return {"message": "Hello, LIFF!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)