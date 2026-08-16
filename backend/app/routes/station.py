from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.station import StationCreate, StationResponse
from app.services import station_service

router = APIRouter(prefix="/stations", tags=["Stations"])

@router.get("/", response_model=List[StationResponse], status_code=status.HTTP_200_OK)
def list_stations(db: Session = Depends(get_db)):
    return station_service.get_all_stations(db)

@router.get("/{station_id}", response_model=StationResponse, status_code=status.HTTP_200_OK)
def get_station(station_id: int, db: Session = Depends(get_db)):
    return station_service.get_station_by_id(db=db, station_id=station_id)

@router.post("/", response_model=StationResponse, status_code=status.HTTP_201_CREATED)
def register_station(station: StationCreate, db: Session = Depends(get_db)):
    return station_service.create_station(db=db, station_data=station)