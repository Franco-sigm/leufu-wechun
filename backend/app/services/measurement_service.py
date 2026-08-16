from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime
from app.models.measurement import MeasurementModel
from app.models.sensor import SensorModel
from app.schemas.measurement import MeasurementCreate

def get_all_measurements(db: Session, skip: int = 0, limit: int = 100):
    return db.query(MeasurementModel).offset(skip).limit(limit).all()

def get_measurements_by_sensor(db: Session, sensor_id: int):
    # Validar que el sensor exista
    sensor = db.query(SensorModel).filter(SensorModel.id == sensor_id).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron mediciones: El sensor con ID {sensor_id} no existe."
        )
    return db.query(MeasurementModel).filter(MeasurementModel.sensor_id == sensor_id).all()

def create_measurement(db: Session, measurement_data: MeasurementCreate):
    # Validar que el sensor emisor exista activamente
    sensor = db.query(SensorModel).filter(SensorModel.id == measurement_data.sensor_id).first()
    if not sensor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se puede registrar la medición porque el sensor con ID {measurement_data.sensor_id} no existe."
        )
    
    try:
        db_measurement = MeasurementModel(
            value=measurement_data.value,
            timestamp=measurement_data.timestamp or datetime.utcnow(),
            sensor_id=measurement_data.sensor_id
        )
        db.add(db_measurement)
        db.commit()
        db.refresh(db_measurement)
        return db_measurement
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al guardar la medición hidrológica: {str(e)}"
        )