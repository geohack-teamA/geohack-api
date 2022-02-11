from fastapi import APIRouter

from app.api.routes import example

router = APIRouter()
router.include_router(example.router, tags=["example"], prefix="/examples")


@router.get("/")
async def hello():
    return {"text": "hello"}
