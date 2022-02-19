from typing import Optional
from fastapi import Response
from pydantic import BaseModel


# ******************************
# Common
# ******************************
class Shelter(BaseModel):
    name: str
    lat: float
    lng: float


class Building(BaseModel):
    id: str
    storeysAboveGround: float
    height: float
    depth: float
    depthRank: float


# ******************************
# Request
# ******************************
class EvacuationRequest(BaseModel):
    lat: float
    lng: float
    currentLevel: int
    hasDifficultFamily: bool
    hasSafeRelative: bool
    hasEnoughStock: bool


# ******************************
# Response
# ******************************
class EvacuationResponse(BaseModel):
    shouldEvacuate: bool = False
    message: str = "hello"
    nearestShelter: Optional[Shelter] = None
    userBuilding: Optional[Building] = None

    class Config:
        arbitrary_types_allowed = True
