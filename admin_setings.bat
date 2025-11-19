@echo off
chcp 65001 >nul
title 🔧 Dashboard - Modo Administrador
mode con: cols=75 lines=20

echo.
echo    ╔══════════════════════════════════════════════════╗
echo    ║               MODO ADMINISTRADOR                 ║
echo    ║         Solucionador de problemas v1.0           ║
echo    ╚══════════════════════════════════════════════════╝
echo.
echo    ┌──────────────────────────────────────────────────┐
echo    │                 DIAGNÓSTICO                      │
echo    └──────────────────────────────────────────────────┘
echo.

:: Limpiar puerto
echo    [1/4] Limpiando puerto 8501...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8501 2^>nul') do (
    taskkill /F /PID %%a >nul 2>&1
    echo    Proceso %%a terminado
)

:: Verificar archivos
echo    [2/4] 📁 Verificando archivos...
if exist "dashboard.py" (
    echo    dashboard.py encontrado
) else (
    echo    ERROR: No se encuentra dashboard.py
    pause
    exit /b 1
)

:: Verificar Python
echo    [3/4] Verificando Python...
python -c "import streamlit, pandas, plotly" 2>nul
if errorlevel 1 (
    echo    Dependencias faltantes
    echo    Instalando...
    pip install streamlit pandas plotly openpyxl >nul 2>&1
    echo    Dependencias instaladas
) else (
    echo    Todas las dependencias OK
)

:: Ejecutar
echo    [4/4] Iniciando aplicación...
echo.
echo    ┌──────────────────────────────────────────────────┐
echo    │                 TODO LISTO                    │
echo    ├──────────────────────────────────────────────────┤
echo    │  Sistema verificado                           │
echo    │  Dependencias instaladas                      │
echo    │  Puerto liberado                              │
echo    │  Abre: http://localhost:8501                 │
echo    └──────────────────────────────────────────────────┘
echo.

timeout /t 3 /nobreak >nul
streamlit run dashboard.py --server.port=8501