from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.sensor import SensorModel
from app.models.station import StationModel
from app.schemas.sensor import SensorCreate

def get_all_sensors(db: Session):
    return db.query(SensorModel).all()

def get_sensors_by_station(db: Session, station_id: int):
    # Validar primero si la estación existe
    station = db.query(StationModel).filter(StationModel.id == station_id).first()
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede listar sensores: La estación con ID {station_id} no existe."
        )
    return db.query(SensorModel).filter(SensorModel.station_id == station_id).all()

def create_sensor(db: Session, sensor_data: SensorCreate):
    # Validar que la estación exista antes de asociar el sensor
    station = db.query(StationModel).filter(StationModel.id == sensor_data.station_id).first()
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede registrar el sensor porque la estación con ID {sensor_data.station_id} no existe."
        )
    
    try:
        db_sensor = SensorModel(
            sensor_type=sensor_data.sensor_type,
            unit=sensor_data.unit,
            is_active=sensor_data.is_active,
            station_id=sensor_data.station_id
        )
        db.add(db_sensor)
        db.commit()
        db.refresh(db_sensor)
        return db_sensor
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al intentar registrar el sensor: {str(e)}"
        )