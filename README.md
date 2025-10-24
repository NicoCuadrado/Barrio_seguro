# Sistema Barrio Seguro
Sistema completo de reconocimiento facial para control de acceso a barrio privado.

## 🏠 Descripción
Sistema avanzado de control de acceso que utiliza reconocimiento facial para identificar vecinos y gestionar visitas en un barrio privado. Desarrollado en Python con OpenCV y face_recognition.

## ✨ Características Principales

### 🎥 Reconocimiento Facial en Tiempo Real
- Detección automática de rostros mediante cámara web
- Reconocimiento de vecinos registrados con alta precisión
- Identificación y registro automático de visitas desconocidas
- Interfaz visual con rectángulos de colores (verde=vecino, rojo=visita)

### 👤 Gestión de Vecinos
- Registro de nuevos vecinos desde cámara o archivo de imagen
- Almacenamiento de codificaciones faciales en base de datos SQLite
- Lista y gestión de vecinos registrados
- Eliminación segura (desactivación) de vecinos

### 🚶 Control de Visitas
- Detección automática de personas desconocidas
- Captura y almacenamiento temporal de fotos de visitas
- Seguimiento de tiempo de permanencia
- Eliminación automática de registros de visitas expiradas

### 📊 Análisis y Reportes
- Estadísticas detalladas de accesos por horas, días y vecinos
- Identificación de horas pico y valle de actividad
- Análisis de patrones de visitas
- Generación de reportes en formato JSON
- Vecinos más activos y frecuencias de acceso

### 💾 Base de Datos Integrada
- SQLite para almacenamiento local seguro
- Tablas optimizadas para vecinos, accesos y visitas temporales
- Respaldo automático y gestión de datos históricos

## 🔧 Tecnologías Utilizadas

### Dependencias Principales
- **Python 3.10+** - Lenguaje base
- **OpenCV (cv2)** - Procesamiento de video e imágenes
- **face_recognition** - Reconocimiento facial avanzado
- **SQLite3** - Base de datos integrada
- **NumPy** - Computación numérica
- **datetime** - Gestión de fechas y horas

### Arquitectura del Proyecto
```
barrio_seguro/
├── dataset/
│   ├── vecinos/          # Imágenes de vecinos registrados
│   └── visitas/          # Fotos temporales de visitas
├── registros/
│   ├── accesos.db       # Base de datos SQLite
│   └── sistema.log      # Logs del sistema
├── main.py              # Archivo principal y menú
├── reconocimiento.py    # Motor de reconocimiento facial
├── registro_vecino.py   # Gestión de vecinos
├── base_datos.py        # Manejo de base de datos
├── analisis_registros.py # Sistema de análisis
├── utils.py             # Utilidades y configuración
└── config.json          # Configuración del sistema
```

## 🚀 Instalación y Configuración

### Prerrequisitos
1. Python 3.10 o superior
2. Cámara web funcional
3. Windows/Linux/macOS

### Instalación de Dependencias
```bash
pip install opencv-python
pip install face_recognition
pip install numpy
```

### Configuración Inicial
1. Descargar/clonar el proyecto en tu directorio deseado
2. Ejecutar `python main.py` para inicializar el sistema
3. El sistema creará automáticamente las carpetas y base de datos necesarias

## 📋 Modo de Uso

### Inicio del Sistema
```bash
python main.py
```

### Funcionalidades Principales

#### 1. 🎥 Reconocimiento en Tiempo Real
- Seleccionar opción 1 en el menú principal
- El sistema abrirá la cámara y comenzará el reconocimiento
- Presionar 'q' para salir, 'r' para registro rápido

#### 2. 👤 Registro de Vecinos
- **Desde cámara**: Captura foto en tiempo real
- **Desde archivo**: Carga imagen desde disco
- Preview automático antes de confirmar registro

#### 3. 📊 Análisis de Datos
- Reportes automáticos de actividad
- Estadísticas por horas, días y vecinos
- Exportación de datos en JSON

### Controles del Sistema
- **Reconocimiento**: `q` salir, `r` registro, `c` limpiar visitas
- **Registro**: `ESPACIO` capturar, `ESC` cancelar
- **Preview**: `ENTER` confirmar, `ESC` cancelar

## ⚙️ Configuración Avanzada

### Parámetros Configurables
```json
{
    "tolerancia_reconocimiento": 0.5,    // Precisión del reconocimiento
    "tiempo_visita_minutos": 30,         // Duración de visitas temporales
    "camara_index": 0,                   // Índice de cámara a usar
    "fps_objetivo": 30,                  // FPS de captura
    "resolucion_camara": [640, 480],     // Resolución de cámara
    "procesar_cada_n_frames": 3          // Optimización de rendimiento
}
```

### Ajustes de Tolerancia
- **0.3-0.4**: Muy estricto (alta seguridad)
- **0.4-0.5**: Equilibrado (recomendado)
- **0.5-0.6**: Permisivo (mayor comodidad)

## 📊 Características del Sistema

### Base de Datos
- **Tabla vecinos**: ID, nombre, ruta_imagen, encoding, fecha_registro, activo
- **Tabla accesos**: ID, nombre, tipo_persona, tipo_evento, fecha_hora, ruta_imagen
- **Tabla visitas_temporales**: ID, nombre_archivo, encoding, fecha_entrada, activa

### Seguridad y Privacidad
- Codificaciones faciales encriptadas en base de datos
- Eliminación automática de datos temporales de visitas
- Logs de seguridad con timestamps
- Acceso controlado a datos sensibles

### Optimizaciones de Rendimiento
- Procesamiento selectivo de frames para mayor fluidez
- Precargas de encodings conocidos
- Redimensionamiento inteligente de imágenes
- Limpieza automática de archivos temporales

## 🔍 Funcionalidades Avanzadas

### Manejo Inteligente de Visitas
- Detección de reingreso de la misma visita
- Registro automático de entrada y salida
- Fotos de seguridad con timestamp
- Limpieza automática tras tiempo límite

### Sistema de Logs
- Registro detallado de todos los eventos
- Niveles de logging configurables
- Rotación automática de archivos de log
- Auditoría completa del sistema

### Análisis Estadístico
- Patrones de comportamiento por vecino
- Identificación de horas pico de actividad
- Tendencias de visitas por día/semana/mes
- Reportes exportables para auditorías

## 🛠️ Solución de Problemas

### Problemas Comunes

#### Cámara No Detectada
- Verificar que la cámara esté conectada
- Probar diferentes índices de cámara (0, 1, 2...)
- Revisar permisos de acceso a cámara

#### Reconocimiento Impreciso
- Ajustar tolerancia en configuración
- Verificar calidad de imagen de registro
- Asegurar buena iluminación

#### Error de Base de Datos
- Verificar permisos de escritura en carpeta
- Eliminar archivo accesos.db para reinicializar
- Revisar logs para errores específicos

### Optimización de Rendimiento
- Usar procesamiento cada N frames
- Reducir resolución de cámara si es necesario
- Limpiar archivos temporales regularmente

## 📈 Escalabilidad

### Para Barrios Grandes
- Base de datos SQLite soporta miles de vecinos
- Optimización automática de consultas
- Índices para búsquedas rápidas

### Futuras Mejoras
- Integración con hardware de acceso (puertas automáticas)
- Notificaciones push para administradores
- Interfaz web para gestión remota
- API REST para integración con otros sistemas
