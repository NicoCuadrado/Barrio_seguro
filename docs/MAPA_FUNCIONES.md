# 🗺️ MAPA DE FUNCIONES - Sistema Barrio Seguro

Este documento te ayudará a ubicar rápidamente dónde está cada funcionalidad del sistema y qué hace cada módulo.

---

## 📂 ESTRUCTURA PROPUESTA DEL PROYECTO

```
Barrio_seguro/
│
├── 📁 src/                          # Código fuente principal
│   ├── 📁 core/                     # Módulos principales del sistema
│   │   ├── reconocimiento.py       # Motor de reconocimiento facial
│   │   ├── registro_vecino.py      # Gestión de vecinos
│   │   └── menu_sistema.py         # Sistema de menús y UI
│   │
│   ├── 📁 database/                 # Gestión de base de datos
│   │   └── base_datos.py           # Operaciones CRUD y accesos
│   │
│   ├── 📁 analysis/                 # Análisis y reportes
│   │   └── analisis_registros.py   # Estadísticas y reportes
│   │
│   └── 📁 utils/                    # Utilidades y helpers
│       ├── config.py                # Gestión de configuración
│       ├── image_processing.py      # Procesamiento de imágenes
│       └── helpers.py               # Funciones auxiliares
│
├── 📁 scripts/                      # Scripts de inicialización
│   ├── inicializar_sistema.py      # Setup inicial del proyecto
│   ├── iniciar.ps1                 # Script de inicio PowerShell
│   └── iniciar.bat                 # Script de inicio CMD
│
├── 📁 docs/                         # Documentación
│   ├── MAPA_FUNCIONES.md           # Este archivo
│   ├── GUIA_DESARROLLO.md          # Guía para desarrolladores
│   └── API_REFERENCE.md            # Referencia de funciones
│
├── 📁 dataset/                      # Datos del sistema
│   ├── 📁 vecinos/                 # Imágenes de vecinos
│   └── 📁 visitas/                 # Imágenes de visitas
│
├── 📁 registros/                    # Logs y base de datos
│   ├── accesos.db                  # Base de datos SQLite
│   └── sistema.log                 # Logs del sistema
│
├── main.py                          # Punto de entrada principal ⭐
├── config.json                      # Configuración del sistema
├── requirements.txt                 # Dependencias
└── README.md                        # Documentación principal
```

---

## 🎯 FUNCIONES POR MÓDULO

### 1️⃣ **main.py** - Punto de Entrada Principal
📍 **Ubicación:** `Barrio_seguro/main.py`

#### Clase Principal:
- **`SistemaBarrioSeguro`** - Orquestador principal del sistema

#### Funciones del Menú:
| Función | Descripción | Línea Aprox. |
|---------|-------------|--------------|
| `__init__()` | Inicializa el sistema completo | ~37 |
| `inicializar_sistema()` | Carga configuración y BD | ~48 |
| `mostrar_bienvenida()` | Pantalla de inicio | ~75 |
| `mostrar_menu_principal()` | Menú principal | ~95 |
| `submenu_gestion_vecinos()` | Menú de gestión de vecinos | ~105 |
| `submenu_analisis()` | Menú de análisis y reportes | ~167 |
| `submenu_configuracion()` | Menú de configuración | ~233 |
| `mostrar_info_sistema()` | Información del sistema | ~328 |
| `ejecutar()` | Loop principal del programa | ~371 |

---

### 2️⃣ **reconocimiento.py** - Motor de Reconocimiento Facial
📍 **Ubicación:** `Barrio_seguro/reconocimiento.py`

#### Clase Principal:
- **`SistemaReconocimiento`** - Sistema de reconocimiento en tiempo real

#### Funciones Clave:

##### 🔧 Inicialización:
| Función | Descripción | Línea Aprox. |
|---------|-------------|--------------|
| `__init__()` | Inicializa el sistema | ~29 |
| `cargar_vecinos_conocidos()` | Precarga vecinos de BD | ~60 |
| `cargar_visitas_temporales()` | Carga visitas activas | ~86 |
| `inicializar_camara()` | Configura la cámara | ~119 |

##### 👁️ Reconocimiento:
| Función | Descripción | Línea Aprox. |
|---------|-------------|--------------|
| `reconocer_persona()` | Identifica persona por encoding | ~154 |
| `procesar_nueva_visita()` | Registra visita desconocida | ~195 |
| `actualizar_ultimo_acceso()` | Registra acceso en BD | ~244 |

##### 🧹 Mantenimiento:
| Función | Descripción | Línea Aprox. |
|---------|-------------|--------------|
| `limpiar_visitas_expiradas()` | Elimina visitas antiguas | ~270 |
| `mostrar_estadisticas_sesion()` | Muestra stats en pantalla | ~305 |

##### 🚀 Ejecución:
| Función | Descripción | Línea Aprox. |
|---------|-------------|--------------|
| `iniciar_reconocimiento()` | Loop principal de reconocimiento | ~330 |
| `modo_registro_rapido()` | Registro rápido durante ejecución | ~452 |
| `finalizar_sistema()` | Cierre seguro del sistema | ~478 |

---

### 3️⃣ **registro_vecino.py** - Gestión de Vecinos
📍 **Ubicación:** `Barrio_seguro/registro_vecino.py`

#### Clase Principal:
- **`RegistroVecino`** - Gestión completa de vecinos

#### Funciones Principales:

##### 📸 Registro:
| Función | Descripción |
|---------|-------------|
| `registrar_desde_camara()` | Captura foto desde cámara |
| `registrar_desde_archivo()` | Registra desde imagen existente |
| `capturar_foto_camara()` | Captura foto con preview |
| `mostrar_preview_imagen()` | Muestra preview antes de guardar |

##### 📋 Consultas:
| Función | Descripción |
|---------|-------------|
| `listar_vecinos_registrados()` | Lista todos los vecinos activos |
| `buscar_vecino()` | Busca vecino por nombre |
| `obtener_info_vecino()` | Obtiene información detallada |

##### 🗑️ Eliminación:
| Función | Descripción |
|---------|-------------|
| `eliminar_vecino()` | Desactiva vecino (soft delete) |
| `eliminar_definitivo()` | Elimina vecino permanentemente |

---

### 4️⃣ **base_datos.py** - Gestión de Base de Datos
📍 **Ubicación:** `Barrio_seguro/base_datos.py`

#### Clase Principal:
- **`BaseDatos`** - Gestor de base de datos SQLite

#### Funciones por Categoría:

##### 🏗️ Inicialización:
| Función | Descripción |
|---------|-------------|
| `__init__()` | Conecta e inicializa BD |
| `crear_tablas()` | Crea estructura de tablas |
| `verificar_estructura()` | Valida integridad de BD |

##### 👤 Vecinos:
| Función | Descripción |
|---------|-------------|
| `registrar_vecino()` | Inserta nuevo vecino |
| `obtener_vecinos_activos()` | Lista vecinos activos |
| `obtener_vecino_por_nombre()` | Busca vecino específico |
| `actualizar_vecino()` | Modifica datos de vecino |
| `desactivar_vecino()` | Soft delete de vecino |
| `eliminar_vecino_definitivo()` | Hard delete de vecino |

##### 📝 Accesos:
| Función | Descripción |
|---------|-------------|
| `registrar_acceso()` | Registra entrada/salida |
| `obtener_accesos_recientes()` | Últimos N accesos |
| `obtener_accesos_por_fecha()` | Accesos en rango de fechas |
| `obtener_estadisticas_accesos()` | Stats generales |

##### 🚶 Visitas Temporales:
| Función | Descripción |
|---------|-------------|
| `registrar_visita_temporal()` | Registra nueva visita |
| `obtener_visitas_temporales_activas()` | Lista visitas activas |
| `desactivar_visita_temporal()` | Marca visita como inactiva |
| `limpiar_visitas_antiguas()` | Elimina visitas expiradas |

---

### 5️⃣ **analisis_registros.py** - Análisis y Reportes
📍 **Ubicación:** `Barrio_seguro/analisis_registros.py`

#### Clase Principal:
- **`AnalisisRegistros`** - Motor de análisis estadístico

#### Funciones de Análisis:

##### 📊 Estadísticas Básicas:
| Función | Descripción |
|---------|-------------|
| `obtener_resumen_general()` | Resumen completo del sistema |
| `contar_accesos_totales()` | Total de accesos registrados |
| `contar_vecinos_activos()` | Vecinos registrados actualmente |

##### ⏰ Análisis Temporal:
| Función | Descripción |
|---------|-------------|
| `analizar_horas_pico()` | Identifica horas con más actividad |
| `analizar_por_dias_semana()` | Distribución por día de semana |
| `analizar_visitas_por_dia()` | Análisis de últimos N días |
| `tendencia_mensual()` | Tendencias a largo plazo |

##### 👥 Análisis de Personas:
| Función | Descripción |
|---------|-------------|
| `analizar_vecinos_mas_activos()` | Top N vecinos más activos |
| `analizar_frecuencia_vecino()` | Patrón de acceso de vecino |
| `analizar_visitas_recurrentes()` | Visitas que regresan |

##### 💾 Reportes:
| Función | Descripción |
|---------|-------------|
| `generar_reporte_completo()` | Reporte JSON completo |
| `generar_reporte_diario()` | Reporte del día actual |
| `generar_reporte_semanal()` | Reporte de última semana |
| `exportar_csv()` | Exporta datos a CSV |
| `mostrar_reporte_consola()` | Muestra reporte en terminal |

---

### 6️⃣ **utils.py** - Utilidades y Helpers
📍 **Ubicación:** `Barrio_seguro/utils.py`

#### Funciones por Categoría:

##### ⚙️ Configuración:
| Función | Descripción |
|---------|-------------|
| `cargar_configuracion()` | Carga config.json |
| `guardar_configuracion()` | Guarda configuración |
| `configurar_logging()` | Setup del sistema de logs |

##### 🖼️ Procesamiento de Imágenes:
| Función | Descripción |
|---------|-------------|
| `validar_imagen()` | Verifica si imagen es válida |
| `obtener_codificacion_facial()` | Extrae encoding de imagen |
| `comparar_caras()` | Compara dos encodings |
| `redimensionar_imagen()` | Redimensiona manteniendo aspecto |
| `dibujar_rectangulo_cara()` | Dibuja rect + etiqueta en frame |

##### 📁 Gestión de Archivos:
| Función | Descripción |
|---------|-------------|
| `generar_nombre_archivo_visita()` | Nombre único para visita |
| `limpiar_archivos_visitas_antiguas()` | Elimina archivos viejos |
| `crear_directorio_si_no_existe()` | Crea carpeta si no existe |

##### 🔧 Utilidades Generales:
| Función | Descripción |
|---------|-------------|
| `verificar_camara()` | Comprueba disponibilidad de cámara |
| `formatear_tiempo_transcurrido()` | Formatea duración |
| `obtener_info_sistema()` | Info de diagnóstico |

---

### 7️⃣ **inicializar_sistema.py** - Setup Inicial
📍 **Ubicación:** `Barrio_seguro/inicializar_sistema.py`

#### Funciones de Inicialización:
| Función | Descripción |
|---------|-------------|
| `crear_estructura_directorios()` | Crea carpetas necesarias |
| `verificar_dependencias()` | Verifica instalación de librerías |
| `crear_base_datos_ejemplo()` | Inicializa BD con datos demo |
| `crear_archivo_informacion()` | Genera archivo de ayuda |
| `verificar_camara()` | Detecta cámara disponible |
| `main()` | Orquesta toda la inicialización |

---

## 🔍 BÚSQUEDA RÁPIDA DE FUNCIONALIDADES

### ❓ "¿Dónde está la función que...?"

#### 🎥 Reconocimiento Facial
- **Inicia el reconocimiento** → `reconocimiento.py` → `iniciar_reconocimiento()`
- **Reconoce una cara** → `reconocimiento.py` → `reconocer_persona()`
- **Dibuja rectángulos** → `utils.py` → `dibujar_rectangulo_cara()`

#### 👤 Gestión de Vecinos
- **Registra vecino con cámara** → `registro_vecino.py` → `registrar_desde_camara()`
- **Lista vecinos** → `registro_vecino.py` → `listar_vecinos_registrados()`
- **Elimina vecino** → `registro_vecino.py` → `eliminar_vecino()`

#### 📊 Análisis y Reportes
- **Genera reportes** → `analisis_registros.py` → `generar_reporte_completo()`
- **Horas pico** → `analisis_registros.py` → `analizar_horas_pico()`
- **Vecinos activos** → `analisis_registros.py` → `analizar_vecinos_mas_activos()`

#### 💾 Base de Datos
- **Registra acceso** → `base_datos.py` → `registrar_acceso()`
- **Obtiene vecinos** → `base_datos.py` → `obtener_vecinos_activos()`
- **Registra visita** → `base_datos.py` → `registrar_visita_temporal()`

#### ⚙️ Configuración
- **Carga config** → `utils.py` → `cargar_configuracion()`
- **Verifica cámara** → `utils.py` → `verificar_camara()`
- **Setup logs** → `utils.py` → `configurar_logging()`

---

## 🎮 FLUJO DE EJECUCIÓN

### Inicio del Sistema:
```
1. main.py → main()
2. SistemaBarrioSeguro.__init__()
3. inicializar_sistema()
   ├── cargar_configuracion() [utils.py]
   ├── BaseDatos() [base_datos.py]
   └── verificar_camara() [utils.py]
4. ejecutar()
5. Loop del menú principal
```

### Reconocimiento Facial:
```
1. Usuario selecciona opción 1
2. SistemaReconocimiento() [reconocimiento.py]
3. cargar_vecinos_conocidos()
4. inicializar_camara()
5. iniciar_reconocimiento()
   ├── Loop de captura de frames
   ├── reconocer_persona()
   │   ├── Comparar con vecinos
   │   └── Si no coincide → procesar_nueva_visita()
   ├── actualizar_ultimo_acceso() [registra en BD]
   └── dibujar_rectangulo_cara()
```

### Registro de Vecino:
```
1. Usuario selecciona opción 2
2. RegistroVecino() [registro_vecino.py]
3. registrar_desde_camara()
   ├── capturar_foto_camara()
   ├── obtener_codificacion_facial() [utils.py]
   └── BaseDatos.registrar_vecino()
```

### Generación de Reportes:
```
1. Usuario selecciona opción 3
2. AnalisisRegistros() [analisis_registros.py]
3. Selección de tipo de análisis
4. Consultas a base_datos.py
5. Procesamiento de datos
6. generar_reporte_completo()
```

---

## 📝 CONSTANTES IMPORTANTES

### En `utils.py`:
```python
TOLERANCIA_RECONOCIMIENTO = 0.5     # Precisión del reconocimiento
TIEMPO_VISITA_MINUTOS = 30          # Duración de visitas
COLOR_VECINO = (0, 255, 0)          # Verde para vecinos
COLOR_VISITA = (0, 0, 255)          # Rojo para visitas
```

### En `config.json`:
```json
{
  "camara_index": 0,
  "tolerancia_reconocimiento": 0.5,
  "tiempo_visita_minutos": 30,
  "fps_objetivo": 30,
  "procesar_cada_n_frames": 3
}
```

---

## 🔧 MODIFICACIONES COMUNES

### Cambiar Tolerancia de Reconocimiento:
- **Archivo:** `config.json` o `utils.py`
- **Variable:** `tolerancia_reconocimiento`
- **Valores:** 0.3 (estricto) a 0.7 (permisivo)

### Cambiar Tiempo de Visita:
- **Archivo:** `config.json` o `utils.py`
- **Variable:** `tiempo_visita_minutos`
- **Unidad:** Minutos

### Cambiar Colores de Detección:
- **Archivo:** `utils.py`
- **Variables:** `COLOR_VECINO`, `COLOR_VISITA`
- **Formato:** BGR (Blue, Green, Red)

### Cambiar Resolución de Cámara:
- **Archivo:** `config.json`
- **Variable:** `resolucion_camara`
- **Formato:** [ancho, alto]

---

## 💡 CONSEJOS PARA MODIFICAR EL CÓDIGO

### ✅ Antes de Modificar:
1. **Lee este mapa** para ubicar la función
2. **Revisa los comentarios** en el código
3. **Prueba en entorno de desarrollo** primero
4. **Haz backup** de la base de datos

### ✅ Después de Modificar:
1. **Prueba la funcionalidad** completa
2. **Verifica los logs** en `registros/sistema.log`
3. **Actualiza la documentación** si es necesario
4. **Haz commit** de tus cambios

---

## 📚 DOCUMENTACIÓN ADICIONAL

- **README.md** - Documentación general del proyecto
- **INSTALACION.md** - Guía de instalación
- **PRIMEROS_PASOS.txt** - Tutorial de uso básico
- **LEEME_PRIMERO.txt** - Guía de inicio rápido

---

## 🆘 PROBLEMAS COMUNES Y SOLUCIONES

### "No encuentro dónde se registran los accesos"
→ `base_datos.py` → función `registrar_acceso()`

### "¿Dónde se dibuja el rectángulo verde/rojo?"
→ `utils.py` → función `dibujar_rectangulo_cara()`

### "¿Cómo cambio la sensibilidad del reconocimiento?"
→ `config.json` → `tolerancia_reconocimiento` O `utils.py` → `TOLERANCIA_RECONOCIMIENTO`

### "¿Dónde se procesa el frame de la cámara?"
→ `reconocimiento.py` → `iniciar_reconocimiento()` (línea ~370-440)

### "¿Cómo se genera un reporte?"
→ `analisis_registros.py` → `generar_reporte_completo()`

---

**Última actualización:** 30 de octubre de 2025  
**Versión del sistema:** 1.0  
**Autor:** Sistema Barrio Seguro

---

> 💡 **TIP:** Usa Ctrl+F en tu editor para buscar rápidamente funciones específicas en este documento.
