from typing import Optional


from pydantic import BaseModel


class UserInfo(BaseModel):
    username: Optional[str] = None
