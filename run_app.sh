#!/bin/bash

# Navegar al directorio donde está la app
APP_DIR="$(cd "$(dirname "$0")"; pwd)"

# Activar entorno virtual
source "$APP_DIR/.venv/bin/activate"

# Ejecutar Streamlit
python3 -m streamlit run "$APP_DIR/dashboard.py"
