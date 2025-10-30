# Script para verificar el estado del sistema Barrio Seguro
# Uso: .\scripts\verificar_estado.ps1

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  VERIFICACION RAPIDA DEL SISTEMA BARRIO SEGURO" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Activar entorno virtual
& ".\venv\Scripts\Activate.ps1"

# Verificar Python
Write-Host "[1/4] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  $([char]0x2713) Python encontrado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  X Python no encontrado" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verificar dependencias
Write-Host "[2/4] Verificando dependencias criticas..." -ForegroundColor Yellow
try {
    python -c "import cv2, face_recognition, numpy" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $([char]0x2713) Todas las dependencias instaladas" -ForegroundColor Green
    } else {
        Write-Host "  X Faltan dependencias" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "  X Error verificando dependencias" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verificar base de datos
Write-Host "[3/4] Verificando base de datos..." -ForegroundColor Yellow
try {
    $dbCheck = python -c "from base_datos import BaseDatos; db = BaseDatos(); v = db.obtener_vecinos_activos(); print(len(v))" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  $([char]0x2713) Base de datos funcional - $dbCheck vecinos activos" -ForegroundColor Green
    } else {
        Write-Host "  X Error en base de datos" -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "  X Error verificando base de datos" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Verificar configuracion
Write-Host "[4/4] Verificando configuracion..." -ForegroundColor Yellow
if (Test-Path "config.json") {
    Write-Host "  $([char]0x2713) Archivo config.json presente" -ForegroundColor Green
} else {
    Write-Host "  ! config.json no encontrado" -ForegroundColor Yellow
}
Write-Host ""

# Resumen final
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  SISTEMA COMPLETAMENTE FUNCIONAL" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Para iniciar el sistema ejecute:" -ForegroundColor Cyan
Write-Host "  .\scripts\iniciar.ps1" -ForegroundColor White
Write-Host ""

Read-Host "Presione Enter para continuar"
