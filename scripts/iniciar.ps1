# Script de inicio para Barrio Seguro
# Ubicación: scripts/iniciar.ps1

# Cambiar al directorio raíz del proyecto
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptPath
Set-Location $projectRoot

Write-Host "===================================" -ForegroundColor Cyan
Write-Host "   SISTEMA BARRIO SEGURO" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Activando entorno virtual..." -ForegroundColor Yellow

# Activar entorno virtual
& .\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Iniciando sistema..." -ForegroundColor Yellow
Write-Host ""

# Ejecutar el sistema
python main.py

Write-Host ""
Write-Host "Sistema finalizado." -ForegroundColor Cyan
pause
