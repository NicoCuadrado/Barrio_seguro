# 📋 RESUMEN DE ORGANIZACIÓN DEL PROYECTO

## ✅ CAMBIOS REALIZADOS

### 1. Documentación Organizada ✅
```
✅ docs/MAPA_FUNCIONES.md        → Mapa completo de todas las funciones
✅ docs/GUIA_REORGANIZACION.md   → Guía para reorganizar el proyecto
✅ docs/PRIMEROS_PASOS.txt       → Tutorial de uso
✅ docs/INSTALACION.md           → Guía de instalación
✅ docs/LEEME_PRIMERO.txt        → Inicio rápido
```

### 2. Scripts Organizados ✅
```
✅ scripts/iniciar.ps1            → Script de inicio PowerShell (actualizado)
✅ scripts/iniciar.bat            → Script de inicio CMD (actualizado)
✅ scripts/inicializar_sistema.py → Setup inicial
```

### 3. Estructura de Carpetas Creada ✅
```
✅ src/core/        → Para módulos principales
✅ src/database/    → Para gestión de BD
✅ src/analysis/    → Para análisis
✅ src/utils/       → Para utilidades
✅ docs/            → Toda la documentación
✅ scripts/         → Todos los scripts
```

---

## 📂 ESTRUCTURA ACTUAL

```
Barrio_seguro/
│
├── 📁 src/                           ✅ Creada (vacía por ahora)
│   ├── core/
│   ├── database/
│   ├── analysis/
│   └── utils/
│
├── 📁 scripts/                       ✅ Organizada
│   ├── inicializar_sistema.py
│   ├── iniciar.ps1
│   └── iniciar.bat
│
├── 📁 docs/                          ✅ Organizada
│   ├── MAPA_FUNCIONES.md            🗺️ TU MEJOR AMIGO
│   ├── GUIA_REORGANIZACION.md       📐 Plan de mejora
│   ├── RESUMEN_ORGANIZACION.md      📋 Este archivo
│   ├── PRIMEROS_PASOS.txt
│   ├── INSTALACION.md
│   └── LEEME_PRIMERO.txt
│
├── 📁 dataset/
│   ├── vecinos/
│   └── visitas/
│
├── 📁 registros/
│   ├── accesos.db
│   └── sistema.log
│
├── main.py                           ⭐ PUNTO DE ENTRADA
├── reconocimiento.py                 🎥 Motor de reconocimiento
├── registro_vecino.py                👤 Gestión de vecinos
├── base_datos.py                     💾 Base de datos
├── analisis_registros.py             📊 Análisis y reportes
├── utils.py                          🔧 Utilidades
├── config.json                       ⚙️ Configuración
├── requirements.txt
└── README.md
```

---

## 🎯 CÓMO USAR EL PROYECTO AHORA

### 1️⃣ Iniciar el Sistema
```powershell
# Opción A: Desde raíz del proyecto
.\scripts\iniciar.ps1

# Opción B: Desde carpeta scripts
cd scripts
.\iniciar.ps1
```

### 2️⃣ Encontrar Funciones
**📖 Lee: `docs/MAPA_FUNCIONES.md`**

Este archivo contiene:
- ✅ Lista completa de todas las funciones
- ✅ Ubicación exacta de cada función
- ✅ Descripción de qué hace cada función
- ✅ Número de línea aproximado
- ✅ Ejemplos de uso

**Ejemplos de búsqueda:**

```
❓ ¿Dónde se reconoce una cara?
✅ reconocimiento.py → reconocer_persona() → Línea ~154

❓ ¿Dónde se dibuja el rectángulo verde?
✅ utils.py → dibujar_rectangulo_cara() → Línea ~247

❓ ¿Dónde se registra un vecino?
✅ registro_vecino.py → registrar_desde_camara() → Clase RegistroVecino

❓ ¿Dónde están los menús?
✅ main.py → SistemaBarrioSeguro → Múltiples funciones de menú

❓ ¿Dónde se guardan los accesos?
✅ base_datos.py → registrar_acceso()
```

### 3️⃣ Modificar el Sistema

**Antes de modificar:**
1. Abre `docs/MAPA_FUNCIONES.md`
2. Busca la función que necesitas modificar (Ctrl+F)
3. Ve al archivo y línea indicados
4. Lee los comentarios en el código
5. Haz tu modificación
6. Prueba que funcione

---

## 🗺️ MAPA RÁPIDO DE FUNCIONES

### 🎥 RECONOCIMIENTO FACIAL → `reconocimiento.py`

| Función | Qué Hace |
|---------|----------|
| `iniciar_reconocimiento()` | Loop principal, abre cámara |
| `reconocer_persona()` | Identifica quién es la persona |
| `procesar_nueva_visita()` | Guarda nueva visita desconocida |
| `cargar_vecinos_conocidos()` | Carga vecinos de la BD |
| `limpiar_visitas_expiradas()` | Elimina visitas viejas |

### 👤 GESTIÓN DE VECINOS → `registro_vecino.py`

| Función | Qué Hace |
|---------|----------|
| `registrar_desde_camara()` | Captura foto y registra |
| `registrar_desde_archivo()` | Registra desde imagen existente |
| `listar_vecinos_registrados()` | Muestra todos los vecinos |
| `eliminar_vecino()` | Desactiva vecino |

### 💾 BASE DE DATOS → `base_datos.py`

| Función | Qué Hace |
|---------|----------|
| `registrar_acceso()` | Guarda entrada/salida |
| `registrar_vecino()` | Inserta nuevo vecino |
| `obtener_vecinos_activos()` | Lista vecinos activos |
| `registrar_visita_temporal()` | Registra visita nueva |

### 📊 ANÁLISIS → `analisis_registros.py`

| Función | Qué Hace |
|---------|----------|
| `generar_reporte_completo()` | Crea reporte JSON |
| `analizar_horas_pico()` | Identifica horas con más accesos |
| `analizar_vecinos_mas_activos()` | Top N vecinos |

### 🔧 UTILIDADES → `utils.py`

| Función | Qué Hace |
|---------|----------|
| `dibujar_rectangulo_cara()` | Dibuja rect verde/rojo |
| `obtener_codificacion_facial()` | Extrae encoding de cara |
| `comparar_caras()` | Compara dos encodings |
| `cargar_configuracion()` | Lee config.json |
| `verificar_camara()` | Verifica si cámara funciona |

### 🎮 MENÚS → `main.py`

| Función | Qué Hace |
|---------|----------|
| `mostrar_menu_principal()` | Muestra menú principal |
| `submenu_gestion_vecinos()` | Menú de vecinos |
| `submenu_analisis()` | Menú de reportes |
| `submenu_configuracion()` | Menú de config |
| `ejecutar()` | Loop principal del programa |

---

## 📝 MODIFICACIONES COMUNES

### Cambiar Colores de Detección

**Archivo:** `utils.py`  
**Líneas:** ~18-21

```python
# Colores actuales (BGR)
COLOR_VECINO = (0, 255, 0)      # Verde
COLOR_VISITA = (0, 0, 255)      # Rojo

# Cambiar a:
COLOR_VECINO = (255, 0, 0)      # Azul
COLOR_VISITA = (0, 165, 255)    # Naranja
```

### Cambiar Tolerancia de Reconocimiento

**Opción 1 - Archivo:** `config.json`
```json
{
  "tolerancia_reconocimiento": 0.4  // Más estricto
}
```

**Opción 2 - Archivo:** `utils.py`, Línea ~15
```python
TOLERANCIA_RECONOCIMIENTO = 0.4
```

### Cambiar Tiempo de Visitas

**Archivo:** `config.json`
```json
{
  "tiempo_visita_minutos": 60  // 1 hora
}
```

### Cambiar Resolución de Cámara

**Archivo:** `config.json`
```json
{
  "resolucion_camara": [1280, 720]  // HD
}
```

### Agregar Funcionalidad al Menú

**Archivo:** `main.py`  
**Función:** `mostrar_menu_principal()` y `ejecutar()`

1. Agregar opción al menú
2. Agregar elif en el loop de ejecutar()
3. Crear función para la nueva funcionalidad

---

## 🚀 PRÓXIMOS PASOS OPCIONALES

### Si Quieres Reorganizar Más (Opcional):

Lee: `docs/GUIA_REORGANIZACION.md`

**Beneficios:**
- Código más profesional
- Más fácil de mantener
- Mejor para trabajar en equipo

**Esfuerzo:** 2-3 horas

**¿Cuándo hacerlo?**
- Cuando tengas tiempo libre
- Antes de hacer cambios grandes
- Si quieres contribuir a GitHub

---

## 💡 CONSEJOS IMPORTANTES

### ✅ SIEMPRE:
1. **Lee `docs/MAPA_FUNCIONES.md` PRIMERO** antes de buscar código
2. **Haz backup** antes de modificar
3. **Prueba después de cada cambio** pequeño
4. **Revisa logs** en `registros/sistema.log` si hay errores

### ❌ NUNCA:
1. Modifiques sin saber qué hace la función
2. Cambies múltiples cosas a la vez
3. Elimines archivos sin backup
4. Ignores los errores en los logs

---

## 🎓 RESUMEN PARA TI

### 📚 Tienes Ahora:

1. **`docs/MAPA_FUNCIONES.md`** → 🗺️ Tu GPS del código
   - Busca cualquier función aquí PRIMERO
   - Tiene líneas aproximadas
   - Tiene descripciones claras

2. **`docs/GUIA_REORGANIZACION.md`** → 📐 Plan de mejora (opcional)
   - Para cuando quieras reorganizar todo
   - Explica pros y contras
   - Paso a paso

3. **Documentación organizada** → 📖 Todo en `docs/`
   - Fácil de encontrar
   - No está mezclada con código

4. **Scripts organizados** → 🎮 Todo en `scripts/`
   - Scripts de inicio actualizados
   - Funcionan desde cualquier lugar

### 🎯 Para Trabajar:

1. **Inicia:** `.\scripts\iniciar.ps1`
2. **Busca función:** Abre `docs/MAPA_FUNCIONES.md` → Ctrl+F
3. **Modifica:** Ve al archivo y línea indicados
4. **Prueba:** Ejecuta y verifica que funcione

---

## 🆘 SI TE PIERDES:

1. **¿No sabes dónde está algo?**
   → `docs/MAPA_FUNCIONES.md`

2. **¿No sabes cómo iniciar?**
   → `.\scripts\iniciar.ps1`

3. **¿Quieres reorganizar todo?**
   → `docs/GUIA_REORGANIZACION.md`

4. **¿Problemas técnicos?**
   → `registros/sistema.log`

---

## ✅ ESTADO FINAL

```
✅ Documentación completa y organizada
✅ Scripts actualizados y funcionando
✅ Mapa de funciones detallado
✅ Estructura base creada para futuro
✅ README actualizado
✅ Sistema 100% funcional
```

---

**¡Todo listo para trabajar!** 🎉

**Empieza aquí:** `docs/MAPA_FUNCIONES.md`

---

Última actualización: 30 de octubre de 2025  
Versión: 1.0  
