from sqlalchemy import Column, Integer, String, Float
from geoalchemy2 import Geometry
from ..core.database import Base

class StationModel(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    river_name = Column(String, index=True, nullable=False)
    comuna = Column(String, nullable=False)
    geom = Column(Geometry(geometry_type='POINT', srid=4326), nullable=False)
    critical_level = Column(Float, default=3.5)