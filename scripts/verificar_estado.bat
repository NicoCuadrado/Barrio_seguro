@echo off
REM Script para verificar el estado del sistema Barrio Seguro
REM Uso: verificar_estado.bat

echo ============================================================
echo   VERIFICACION RAPIDA DEL SISTEMA BARRIO SEGURO
echo ============================================================
echo.

REM Activar entorno virtual
call venv\Scripts\activate.bat

REM Verificar Python
echo [1/4] Verificando Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo   X Python no encontrado
    goto :error
) else (
    echo   OK Python encontrado
)
echo.

REM Verificar dependencias
echo [2/4] Verificando dependencias criticas...
python -c "import cv2, face_recognition, numpy" 2>nul
if %errorlevel% neq 0 (
    echo   X Faltan dependencias
    goto :error
) else (
    echo   OK Todas las dependencias instaladas
)
echo.

REM Verificar base de datos
echo [3/4] Verificando base de datos...
python -c "from base_datos import BaseDatos; db = BaseDatos(); v = db.obtener_vecinos_activos(); print('  OK Base de datos funcional -', len(v), 'vecinos activos')" 2>nul
if %errorlevel% neq 0 (
    echo   X Error en base de datos
    goto :error
)
echo.

REM Verificar configuracion
echo [4/4] Verificando configuracion...
if exist config.json (
    echo   OK Archivo config.json presente
) else (
    echo   ! config.json no encontrado
)
echo.

echo ============================================================
echo   SISTEMA COMPLETAMENTE FUNCIONAL
echo ============================================================
echo.
echo Para iniciar el sistema ejecute:
echo   scripts\iniciar.bat
echo.
pause
exit /b 0

:error
echo.
echo ============================================================
echo   ERROR EN LA VERIFICACION
echo ============================================================
echo.
echo Revise los errores anteriores e intente:
echo   1. Reinstalar dependencias: pip install -r requirements.txt
echo   2. Verificar entorno virtual: venv\Scripts\activate.bat
echo   3. Consultar documentacion en docs\
echo.
pause
exit /b 1
