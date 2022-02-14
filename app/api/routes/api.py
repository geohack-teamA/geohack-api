from aiohttp import request
from fastapi import APIRouter
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from app.api.routes import example
from app.core.config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

router = APIRouter()
router.include_router(example.router, tags=["example"], prefix="/examples")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@router.get("/")
async def hello():
    try:
        line_bot_api.broadcast(TextSendMessage(text="Hello!!!"))
    except LineBotApiError as e:
        print(e)
    return {"text": "hello"}
