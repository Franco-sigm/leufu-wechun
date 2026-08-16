from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SensorModel(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)
    station_id = Column(Integer, ForeignKey("stations.id"), nullable=False)
    sensor_type = Column(String, nullable=False)  # Ej: "nivel_agua", "caudal"
    unit = Column(String, nullable=False)        # Ej: "m", "m3/s"

    station = relationship("StationModel", backref="sensors")