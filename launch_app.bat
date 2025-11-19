@echo off
chcp 65001 >nul
title Dashboard Compras/Ventas

:: Fuerza a cambiar al directorio donde está este .bat
pushd "%~dp0"

echo.
echo    ╔══════════════════════════════════════════════╗
echo    ║              INICIANDO DASHBOARD          ║
echo    ║           Compras y Ventas v1.0              ║
echo    ╚══════════════════════════════════════════════╝
echo.
echo    ┌──────────────────────────────────────────────┐
echo    │              VERIFICANDO ARCHIVOS         │
echo    └──────────────────────────────────────────────┘
echo.

echo    Directorio actual: %CD%
echo    Buscando archivos Python...
dir *.py >nul 2>&1

if not exist "dashboard.py" (
    echo.
    echo    ERROR: No se encuentra dashboard.py
    echo.
    echo    ┌──────────────────────────────────────────────┐
echo    │              ARCHIVOS ENCONTRADOS         │
echo    └──────────────────────────────────────────────┘
    dir *.py /b
    echo.
    echo    ┌──────────────────────────────────────────────┐
echo    │               SOLUCIONES                 │
echo    └──────────────────────────────────────────────┘
    echo    1. Asegúrate de que dashboard.py esté en la misma carpeta
    echo    2. Verifica que el nombre sea EXACTAMENTE "dashboard.py"
    echo.
    pause
    exit /b 1
)

echo.
echo    [OK] dashboard.py encontrado
echo    Iniciando aplicación...
echo.
echo    ┌──────────────────────────────────────────────┐
echo    │              INSTRUCCIONES                   │
echo    └──────────────────────────────────────────────┘
echo.
echo    1. Tu applicación debe estar ejecutandose en: http://localhost:8501
echo    2. Para cerrar: Ctrl + C en esta ventana
echo.
echo    Iniciando...
echo.

streamlit run dashboard.py --server.port=8501

popd
pause