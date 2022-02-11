from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import TEXT

from app.models.main import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(TEXT, unique=True, nullable=False)
