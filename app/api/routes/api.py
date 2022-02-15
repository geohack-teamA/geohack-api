from sqlalchemy import false
from aiohttp import request
from app.dependencies.gcp.storage import GoogleCloudStorage
from app.models.alert_level import AlertLevel
from app.schemas.evacuation import Evacuation
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
    # try:
    #     line_bot_api.broadcast(
    #         TextSendMessage(text="Hello!!!, http://localhost:3000/form")
    #     )
    # except LineBotApiError as e:
    #     print(e)
    return {"text": "hello"}


@router.get("/form", response_model=Evacuation)
async def form():
    should_evacuate = Evacuation(should_evacuate=False)
    return should_evacuate
    # return {"hoge": "fuga"}


@router.get("/static")
async def test():
    storage = GoogleCloudStorage()
    storage.ls()
    return {"hello": "Helo"}


def get_alert_level() -> AlertLevel:
    alert_level = AlertLevel.THREE
    return alert_level
