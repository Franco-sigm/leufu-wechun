from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.sensor import SensorCreate, SensorResponse
from app.services import sensor_service

router = APIRouter(prefix="/sensors", tags=["Sensors"])

@router.get("/", response_model=List[SensorResponse], status_code=status.HTTP_200_OK)
def list_sensors(db: Session = Depends(get_db)):
    return sensor_service.get_all_sensors(db)

@router.get("/station/{station_id}", response_model=List[SensorResponse], status_code=status.HTTP_200_OK)
def list_sensors_by_station(station_id: int, db: Session = Depends(get_db)):
    return sensor_service.get_sensors_by_station(db=db, station_id=station_id)

@router.post("/", response_model=SensorResponse, status_code=status.HTTP_201_CREATED)
def register_sensor(sensor: SensorCreate, db: Session = Depends(get_db)):
    return sensor_service.create_sensor(db=db, sensor_data=sensor)