@echo off
REM Script de inicio para Barrio Seguro
REM Ubicación: scripts/iniciar.bat

REM Cambiar al directorio raíz del proyecto
cd /d %~dp0\..

echo ===================================
echo   SISTEMA BARRIO SEGURO
echo ===================================
echo.
echo Activando entorno virtual...
call venv\Scripts\activate.bat
echo.
echo Iniciando sistema...
python main.py
pause
