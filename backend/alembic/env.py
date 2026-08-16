import sys
import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context


# ============================================================
# CONFIGURACIÓN DE RUTA ABSOLUTA PARA EL BACKEND
# ============================================================

# Ruta de la carpeta alembic/
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta de la carpeta backend/
backend_dir = os.path.dirname(current_dir)

# Agregamos backend/ al PYTHONPATH
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)


# ============================================================
# IMPORTAR BASE Y MODELOS
# ============================================================

from app.core.database import Base
from app.models.station import StationModel
from app.models.sensor import SensorModel
from app.models.measurement import MeasurementModel


# ============================================================
# CONFIGURACIÓN DE ALEMBIC
# ============================================================

config = context.config


# Configuración de logging desde alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata de SQLAlchemy que Alembic utilizará
target_metadata = Base.metadata


# ============================================================
# FILTRO DE TABLAS
# ============================================================

def include_object(object, name, type_, reflected, compare_to):
    """
    Indica qué objetos debe considerar Alembic durante
    --autogenerate.

    spatial_ref_sys pertenece a PostGIS y no debe ser
    gestionada por las migraciones de nuestra aplicación.
    """

    if type_ == "table" and name == "spatial_ref_sys":
        return False

    return True


# ============================================================
# MIGRACIONES OFFLINE
# ============================================================

def run_migrations_offline() -> None:
    """
    Ejecuta las migraciones sin establecer una conexión
    directa con la base de datos.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named"
        },
        include_object=include_object,
    )

    with context.begin_transaction():
        context.run_migrations()


# ============================================================
# MIGRACIONES ONLINE
# ============================================================

def run_migrations_online() -> None:
    """
    Ejecuta las migraciones conectándose directamente
    a PostgreSQL.
    """

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {}
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_object=include_object,
        )

        with context.begin_transaction():
            context.run_migrations()


# ============================================================
# EJECUTAR MIGRACIONES
# ============================================================

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()