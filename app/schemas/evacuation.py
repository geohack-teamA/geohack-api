from typing import Optional
from pydantic import BaseModel


class Shelter(BaseModel):
    name: str
    lat: float
    lng: float


class Building(BaseModel):
    id: str
    storeys_above_ground: float
    height: float
    depth: float
    depth_rank: float


class EvacuationResponse(BaseModel):
    shouldEvacuate: bool = False
    message: str = "hello"
    nearestShelter: Optional[Shelter] = None
    # userBuilding: Optional[Building] = None

    class Config:
        arbitrary_types_allowed = True


class EvacuationRequest(BaseModel):
    lat: float
    lng: float
    currentLevel: int
    hasDifficultFamily: bool
    hasSafeRelative: bool
    hasEnoughStock: bool
