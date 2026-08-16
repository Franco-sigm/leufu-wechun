from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.measurement import MeasurementCreate, MeasurementResponse
from app.services import measurement_service

router = APIRouter(prefix="/measurements", tags=["Measurements"])

@router.get("/", response_model=List[MeasurementResponse], status_code=status.HTTP_200_OK)
def list_measurements(
    skip: int = Query(0, description="Registros a omitir (paginación)"), 
    limit: int = Query(100, description="Límite de registros a retornar"), 
    db: Session = Depends(get_db)
):
    return measurement_service.get_all_measurements(db, skip=skip, limit=limit)

@router.get("/sensor/{sensor_id}", response_model=List[MeasurementResponse], status_code=status.HTTP_200_OK)
def list_measurements_by_sensor(sensor_id: int, db: Session = Depends(get_db)):
    return measurement_service.get_measurements_by_sensor(db=db, sensor_id=sensor_id)

@router.post("/", response_model=MeasurementResponse, status_code=status.HTTP_201_CREATED)
def register_measurement(measurement: MeasurementCreate, db: Session = Depends(get_db)):
    return measurement_service.create_measurement(db=db, measurement_data=measurement)