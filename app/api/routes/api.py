from app.dependencies.gcp.storage import GoogleCloudStorage
from app.schemas.evacuation import (
    Building,
    EvacuationRequest,
    EvacuationResponse,
    Shelter,
)
from app.service.evacuation import UserAttribute, UserEvacuationJudgement
from app.service.geospatial import GeospatialAnalyzer
from fastapi import APIRouter
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError
from linebot.models import TextSendMessage
from app.core.config import LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

router = APIRouter()

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@router.get("/notify")
async def notify():
    try:
        line_bot_api.broadcast(
            TextSendMessage(
                text="近所で洪水が起こりましたか？今すぐ身の安全を確保しましょう！【ナラデハ】はあなたに最適な水害対策を提案します。以下のリンクから対策診断ページへ進みましょう。https://naradeha.netlify.app "
            )
        )
    except LineBotApiError as e:
        print(e)
    return {"message": "Notification has been sent"}


@router.post("/analyze", response_model=EvacuationResponse)
async def analyze(evacuation_req: EvacuationRequest):
    storage = GoogleCloudStorage()

    # ***Params from client side***
    lat = evacuation_req.lat
    lng = evacuation_req.lng
    current_floor_level = evacuation_req.currentLevel
    has_difficulty_with_family = evacuation_req.hasDifficultFamily
    enough_stock = evacuation_req.hasEnoughStock
    has_safe_relative = evacuation_req.hasSafeRelative
    mesh_level = 3

    geospatia_analyzer = GeospatialAnalyzer(storage, mesh_level)  # noqa
    user_attribute = UserAttribute(
        lat,
        lng,
        current_floor_level,
        has_difficulty_with_family,
        enough_stock,
    )
    user_evacuation_judgement = UserEvacuationJudgement(
        user_attribute, geospatia_analyzer
    )

    # ***Results of analysis***
    (
        should_evacuate,
        message,
        shelter,
        building,
    ) = user_evacuation_judgement.judge_what_user_should_do()
    response = EvacuationResponse(
        shouldEvacuate=should_evacuate,
        message=message,
        nearestShelter=None
        if shelter is None
        else Shelter(name=shelter.name, lat=shelter.lat, lng=shelter.lng),
        userBuilding=None
        if building is None
        else Building(
            id=building.id,
            storeysAboveGround=building.storeys_above_ground,
            height=building.height,
            depth=building.depth,
            depthRank=building.depth_rank,
        ),
    )
    return response
