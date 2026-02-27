@echo off
echo ----------------------------------------------------------------------
echo  INSTALADOR AUTOMATICO - PROYECTO MENU GENERATOR
echo ----------------------------------------------------------------------
echo.
echo 1. Instalando librerias necesarias...
"%LOCALAPPDATA%\Programs\Python\Python313\python.exe" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] No se pudo instalar las librerias.
    echo Verifique su conexion a internet o la instalacion de Python.
    pause
    exit /b %errorlevel%
)

echo.
echo 2. Creando carpetas del proyecto...
"%LOCALAPPDATA%\Programs\Python\Python313\python.exe" setup_project.py

echo.
echo ----------------------------------------------------------------------
echo  [EXITO] Todo listo. Ahora ejecuta run_app.bat
echo ----------------------------------------------------------------------
pause
