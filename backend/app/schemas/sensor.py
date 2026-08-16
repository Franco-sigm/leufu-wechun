from pydantic import BaseModel

class SensorBase(BaseModel):
    sensor_type: str
    unit: str

class SensorCreate(SensorBase):
    station_id: int

class SensorResponse(SensorBase):
    id: int
    station_id: int

    class Config:
        from_attributes = True