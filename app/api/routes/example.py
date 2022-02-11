from typing import Optional
from fastapi import APIRouter

from app.schemas.users import UserInfo

router = APIRouter()


@router.get("/info", response_model=UserInfo, name="users:get-user-info")
async def get_user_info() -> Optional[UserInfo]:
    pass


@router.get("/")
async def hello():
    return {"text": "hello example"}
