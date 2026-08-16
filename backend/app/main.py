from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import engine, Base
from app.models.station import StationModel
from app.models.sensor import SensorModel
from app.models.measurement import MeasurementModel


app = FastAPI(
    title="API Monitoreo de Ríos - La Araucanía",
    version="1.0.0",
    description="Sistema de monitoreo hidrológico y alertas tempranas"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Monitoreo de Ríos de La Araucanía 🌊"}