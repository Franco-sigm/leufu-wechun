from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.station import StationModel
from app.schemas.station import StationCreate

def get_all_stations(db: Session):
    return db.query(StationModel).all()

def get_station_by_id(db: Session, station_id: int):
    station = db.query(StationModel).filter(StationModel.id == station_id).first()
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La estación con ID {station_id} no fue encontrada."
        )
    return station

def create_station(db: Session, station_data: StationCreate):
    # Validar si ya existe una estación con el mismo nombre
    existing = db.query(StationModel).filter(StationModel.name == station_data.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una estación registrada con el nombre '{station_data.name}'."
        )
    
    try:
        # Creación del modelo (Nota: para PostGIS puedes formatear la geometría con ST_GeomFromText)
        db_station = StationModel(
            name=station_data.name,
            river_name=station_data.river_name,
            comuna=station_data.comuna,
            critical_level=station_data.critical_level,
            # geom=f'SRID=4326;POINT({station_data.longitude} {station_data.latitude})'
        )
        db.add(db_station)
        db.commit()
        db.refresh(db_station)
        return db_station
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al intentar guardar la estación: {str(e)}"
        )