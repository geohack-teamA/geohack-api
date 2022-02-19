from app.dependencies.gcp.storage import GoogleCloudStorage
from app.models.alert_level import AlertLevel
from app.schemas.evacuation import (
    Building,
    EvacuationRequest,
    EvacuationResponse,
    Shelter,
)
from app.service.evacuation import Position, UserAttribute, UserEvacuationJudgement
from app.service.geospatial import GeospatialAnalyzer
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


@router.get("/notify")
async def notify():
    try:
        line_bot_api.broadcast(
            TextSendMessage(
                text="近所で洪水が起こりましたか？今すぐ身の安全を確保しましょう！【ナラデハ】はあなたに最適な水害対策を提案します。以下のリンクから対策診断ページへ進みましょう。, http://localhost:3000/form"
            )
        )
    except LineBotApiError as e:
        print(e)
    return {"text": "hello"}


@router.get("/form", response_model=EvacuationResponse)
async def form():
    result = EvacuationResponse(
        shouldEvacuate=False,
        message="hellololo",
        nearestShelter=None,
        userBuilding=None,
    )
    return result


@router.post("/analyze", response_model=EvacuationResponse)
async def analyze(evacuation_req: EvacuationRequest):
    storage = GoogleCloudStorage()
    lat = 35.60044590382672
    lng = 139.6295136313999
    current_floor_level = 4
    has_difficulty_with_family = False
    enough_stock = False
    mesh_level = 3
    print("lat----------", evacuation_req.lat)
    geospatia_analyzer = GeospatialAnalyzer(storage, mesh_level)
    user_attribute = UserAttribute(
        lat,
        lng,
        current_floor_level,
        has_difficulty_with_family,
        enough_stock,
    )
    current_alert_level = AlertLevel.THREE
    user_evacuation_judgement = UserEvacuationJudgement(
        user_attribute, current_alert_level, geospatia_analyzer
    )
    shelter, building = user_evacuation_judgement.judge_what_user_should_do()

    result = EvacuationResponse(
        shouldEvacuate=False,
        message="hellololo",
        nearestShelter=None
        if shelter is None
        else Shelter(name=shelter.name, lat=shelter.lat),
        userBuilding=None if building is None else Building(),
    )
    return result
