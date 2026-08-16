from pydantic import BaseModel

class StationBase(BaseModel):
    name: str
    river_name: str
    comuna: str
    critical_level: float

class StationCreate(StationBase):
    latitude: float
    longitude: float

class StationResponse(StationBase):
    id: int

    class Config:
        from_attributes = True