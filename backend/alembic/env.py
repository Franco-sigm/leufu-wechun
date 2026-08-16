import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# --- CONFIGURACIÓN DE RUTA ABSOLUTA PARA EL BACKEND ---
# Obtenemos la ruta absoluta de la carpeta 'backend' (dos niveles arriba de env.py: alembic/ -> backend/)
current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir)

# Insertamos la ruta al principio del path de Python
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)
# ------------------------------------------------------

# Importar la Base y los modelos de la aplicación
from app.core.database import Base
from app.models.station import StationModel
from app.models.sensor import SensorModel
from app.models.measurement import MeasurementModel

# El resto de tu archivo env.py continúa exactamente igual...
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()