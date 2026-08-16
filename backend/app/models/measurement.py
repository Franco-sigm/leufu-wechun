from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class MeasurementModel(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    sensor_id = Column(Integer, ForeignKey("sensors.id"), nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    sensor = relationship("SensorModel", backref="measurements")