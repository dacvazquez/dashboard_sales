@echo off
chcp 65001 >nul
title Dashboard Compras/Ventas - Instalador
mode con: cols=80 lines=25

echo.
echo    ╔══════════════════════════════════════════════════════════════╗
echo    ║                   DASHBOARD COMERCIAL                        ║
echo    ║                 Compras y Ventas v1.0                        ║
echo    ╚══════════════════════════════════════════════════════════════╝
echo.
echo    ┌──────────────────────────────────────────────────────────────┐
echo    │                     INSTALACIÓN                              │
echo    └──────────────────────────────────────────────────────────────┘
echo.

:: Verificar Python
echo    [1/3] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo    ERROR: Python no encontrado
    echo.
    echo    Descarga Python desde: https://python.org
    echo    Marca "Add Python to PATH" durante la instalación
    echo    Luego vuelve a ejecutar este archivo.
    echo.
    timeout /t 10 /nobreak >nul
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVERSION=%%i
echo    %PYVERSION% detectado

:: Instalar dependencias
echo    [2/3] Instalando dependencias...
echo    Esto puede tomar unos minutos...
echo.

pip install --upgrade pip >nul 2>&1
pip install streamlit pandas plotly openpyxl

if errorlevel 1 (
    echo    Error en la instalación
    echo    Ejecuta como Administrador e intenta nuevamente
    pause
    exit /b 1
)

echo    Dependencias instaladas correctamente
echo.
echo ========================================
echo    INSTALACION COMPLETADA
echo ========================================
echo.
echo 2. Para cerrar: Presiona Ctrl+C en la ventana negra
echo.
pause


