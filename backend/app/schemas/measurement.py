from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MeasurementBase(BaseModel):
    value: float = Field(..., example=2.45, description="Valor numérico de la medición (ej. metros o m³/s)")
    timestamp: Optional[datetime] = Field(None, example="2026-08-16T14:30:00", description="Fecha y hora de la lectura (opcional, por defecto usa la actual)")

class MeasurementCreate(MeasurementBase):
    sensor_id: int = Field(..., example=1, description="ID del sensor que emitió la lectura")

class MeasurementResponse(MeasurementBase):
    id: int
    sensor_id: int
    timestamp: datetime

    class Config:
        from_attributes = True