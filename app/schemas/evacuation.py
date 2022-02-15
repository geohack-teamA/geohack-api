from pydantic import BaseModel


class Evacuation(BaseModel):
    should_evacuate: bool = False
