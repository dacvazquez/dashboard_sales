import subprocess
import sys
import os

# Nombre de tu archivo principal
app = "tu_archivo.py"  # cámbialo por el nombre real

# Arranca Streamlit
subprocess.run([sys.executable, "-m", "streamlit", "run", app])
