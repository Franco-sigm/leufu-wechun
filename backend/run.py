import os
import sys

# Forzar al sistema operativo y a Python a reconocer la carpeta actual como raíz
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["app"]  # Le decimos exactamente dónde vigilar los cambios
    )