from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar los routers de cada módulo
from app.routers import stations, sensors, measurements

app = FastAPI(
    title="API Monitoreo de Ríos - La Araucanía",
    version="1.0.0",
    description="Sistema de monitoreo hidrológico y alertas tempranas"
)

# Configuración de CORS para permitir peticiones del frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, ajusta esto a tu dominio o IP específica
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de la API
app.include_router(stations.router)
app.include_router(sensors.router)
app.include_router(measurements.router)

@app.get("/")
def read_root():
    return {"message": "Bienvenido a la API de Monitoreo de Ríos de La Araucanía 🌊"}