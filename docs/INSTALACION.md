# 🏠 Barrio Seguro - Guía de Instalación Rápida

## ✅ PROBLEMA RESUELTO

El entorno virtual estaba corrupto porque apuntaba a una ubicación anterior. Se ha creado un nuevo entorno virtual limpio y todas las dependencias han sido instaladas correctamente.

## 📦 Dependencias Instaladas

- ✅ Python 3.11.9
- ✅ OpenCV 4.12.0
- ✅ face_recognition 1.3.0
- ✅ dlib 20.0.0
- ✅ numpy 2.2.6
- ✅ Pillow 12.0.0
- ✅ pandas 2.3.3
- ✅ matplotlib 3.10.7

## 🚀 Cómo Iniciar el Sistema

### Opción 1: Usar el script de inicio (RECOMENDADO)

**En PowerShell:**
```powershell
.\iniciar.ps1
```

**En CMD:**
```cmd
iniciar.bat
```

### Opción 2: Manual

1. **Activar el entorno virtual:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Ejecutar el sistema:**
   ```powershell
   python main.py
   ```

## 📋 Estructura del Proyecto

```
Barrio_seguro/
├── venv/                    # Entorno virtual (NUEVO - funcionando correctamente)
├── dataset/
│   ├── vecinos/            # Fotos de vecinos registrados
│   └── visitas/            # Fotos temporales de visitas
├── registros/
│   ├── accesos.db         # Base de datos SQLite
│   └── sistema.log        # Logs del sistema
├── main.py                # Archivo principal ⭐
├── reconocimiento.py      # Motor de reconocimiento facial
├── registro_vecino.py     # Gestión de vecinos
├── base_datos.py          # Manejo de base de datos
├── analisis_registros.py  # Sistema de análisis
├── utils.py               # Utilidades
├── config.json            # Configuración del sistema
├── iniciar.ps1            # Script de inicio PowerShell ⭐
└── iniciar.bat            # Script de inicio CMD ⭐
```

## 🎯 Primeros Pasos

1. **Iniciar el sistema:**
   ```powershell
   .\iniciar.ps1
   ```

2. **Seleccionar opción 2** para registrar vecinos (necesario antes de usar reconocimiento)

3. **Seleccionar opción 1** para iniciar el reconocimiento facial

4. **Controles durante el reconocimiento:**
   - `q` - Salir del reconocimiento
   - `r` - Registro rápido
   - `c` - Limpiar visitas

## ⚙️ Configuración

El archivo `config.json` contiene:
- `camara_index`: 0 (cámara detectada automáticamente)
- `tolerancia_reconocimiento`: 0.5 (ajustable entre 0.3-0.7)
- `tiempo_visita_minutos`: 30
- Y más opciones configurables...

## 🔧 Solución de Problemas

### Si la cámara no funciona:
1. Verificar que la cámara esté conectada
2. Ajustar `camara_index` en `config.json` (probar 0, 1, 2)
3. Reiniciar el sistema

### Si el reconocimiento es impreciso:
- Ajustar `tolerancia_reconocimiento` en `config.json`
- Valores menores = más estricto (0.3-0.4)
- Valores mayores = más permisivo (0.5-0.6)

### Si necesita reinstalar dependencias:
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📊 Funcionalidades Principales

1. **🎥 Reconocimiento Facial en Tiempo Real**
   - Detecta vecinos registrados (rectángulo verde)
   - Identifica visitas desconocidas (rectángulo rojo)
   - Registro automático de accesos

2. **👤 Gestión de Vecinos**
   - Registro desde cámara o archivo
   - Lista de vecinos activos
   - Eliminación segura

3. **📈 Análisis y Reportes**
   - Estadísticas de accesos
   - Horas pico y valle
   - Vecinos más activos
   - Exportación a JSON

4. **💾 Base de Datos**
   - SQLite integrada
   - Registro de todos los accesos
   - Gestión de visitas temporales

## 📱 Contacto y Soporte

- Revisar archivo `PRIMEROS_PASOS.txt` para más detalles
- Consultar `README.md` para documentación completa
- Los logs del sistema se guardan en `registros/sistema.log`

---

**Estado del Sistema:** ✅ FUNCIONANDO CORRECTAMENTE

**Última actualización:** 28 de octubre de 2025
