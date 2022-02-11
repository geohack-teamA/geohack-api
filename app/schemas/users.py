from typing import Optional

from sqlalchemy import null

from pydantic import BaseModel


class UserInfo(BaseModel):
    username: Optional[str] = None

