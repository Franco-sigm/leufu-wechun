from pydantic import BaseModel, Field
from typing import Optional

class SensorBase(BaseModel):
    sensor_type: str = Field(..., example="Nivel de Agua")
    unit: str = Field(..., example="metros")
    is_active: Optional[bool] = Field(True, example=True)

class SensorCreate(SensorBase):
    station_id: int = Field(..., example=1, description="ID de la estación a la que pertenece el sensor")

class SensorResponse(SensorBase):
    id: int
    station_id: int

    class Config:
        from_attributes = True