from pydantic import BaseModel
from datetime import datetime

class MeasurementBase(BaseModel):
    value: float

class MeasurementCreate(MeasurementBase):
    sensor_id: int

class MeasurementResponse(MeasurementBase):
    id: int
    sensor_id: int
    timestamp: datetime

    class Config:
        from_attributes = Truecd back