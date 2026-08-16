from pydantic import BaseModel, Field
from typing import Optional

class StationBase(BaseModel):
    name: str = Field(..., example="Estación Río Trancura")
    river_name: str = Field(..., example="Trancura")
    comuna: str = Field(..., example="Pucón")
    critical_level: float = Field(..., example=3.5)

class StationCreate(StationBase):
    # Aquí puedes añadir latitud y longitud para armar la geometría PostGIS
    latitude: float = Field(..., example=-39.278)
    longitude: float = Field(..., example=-71.971)

class StationResponse(StationBase):
    id: int

    class Config:
        from_attributes = True