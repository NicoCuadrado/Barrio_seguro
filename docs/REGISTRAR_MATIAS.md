# 🎯 Guía Rápida: Registrar a "Matias" como Vecino

## ✅ Problema Solucionado

El vecino "Matias" que existía como **registro inactivo fantasma** ha sido **eliminado completamente** de la base de datos. Ahora puedes registrarlo sin problemas.

---

## 🚀 Cómo Registrar a Matias

### Método 1: Desde Cámara (Recomendado)

1. **Iniciar el sistema:**
   ```powershell
   .\scripts\iniciar.ps1
   ```

2. **Navegar al menú de registro:**
   - Selecciona: `1. Gestión de Vecinos`
   - Luego: `1. Registrar nuevo vecino (cámara)`

3. **Ingresar el nombre:**
   - Cuando pida el nombre, escribe: `Matias`
   - Presiona Enter

4. **Capturar la foto:**
   - La cámara se abrirá automáticamente
   - Posiciónate frente a la cámara
   - Presiona `ESPACIO` para capturar
   - Se mostrará un preview
   - Presiona `ENTER` para confirmar o `ESC` para reintentar

5. **Confirmar registro:**
   - ✅ Verás: "Vecino 'Matias' registrado exitosamente"
   - La foto se guardará en `dataset/vecinos/Matias.jpg`

---

### Método 2: Desde Archivo de Imagen

Si ya tienes una foto de Matias:

1. **Preparar la imagen:**
   - Asegúrate de que sea una foto clara del rostro
   - Formatos soportados: `.jpg`, `.jpeg`, `.png`
   - La cara debe ser visible y estar bien iluminada

2. **Iniciar el sistema:**
   ```powershell
   .\scripts\iniciar.ps1
   ```

3. **Navegar al menú:**
   - Selecciona: `1. Gestión de Vecinos`
   - Luego: `2. Registrar nuevo vecino (desde archivo)`

4. **Ingresar datos:**
   - Nombre: `Matias`
   - Ruta del archivo: (ruta completa a la imagen)
   
   Ejemplo:
   ```
   C:\Users\Matias\Pictures\foto_matias.jpg
   ```

5. **Confirmar registro:**
   - Se mostrará un preview de la imagen
   - Presiona `ENTER` para confirmar
   - ✅ "Vecino 'Matias' registrado exitosamente"

---

## 🔍 Verificar que Matias fue Registrado

### Opción 1: Listar Vecinos

1. Desde el menú principal: `1. Gestión de Vecinos`
2. Selecciona: `3. Listar vecinos registrados`
3. Deberías ver a "Matias" en la lista

### Opción 2: Probar Reconocimiento

1. Desde el menú principal: `1. Iniciar reconocimiento facial`
2. Párate frente a la cámara
3. Deberías ver un **rectángulo verde** con el nombre "Matias"

### Opción 3: Verificar en Base de Datos

Ejecuta:
```powershell
python -c "from base_datos import BaseDatos; db = BaseDatos(); vecinos = db.obtener_vecinos_activos(); print('Vecinos:', [v[0] for v in vecinos])"
```

Deberías ver algo como:
```
Vecinos: [2, 3, 4]  # El ID de Matias será el más alto
```

---

## 📋 Vecinos Actualmente Registrados

Antes de registrar a Matias:
- M (ID: 2)
- Mati (ID: 3)

Después de registrar a Matias:
- M (ID: 2)
- Mati (ID: 3)
- **Matias (ID: 4)** ✅ NUEVO

---

## ⚠️ Solución de Problemas

### "El nombre ya existe"
Si aún ves este error:
1. Ejecuta: `.\scripts\verificar_estado.ps1`
2. Si el problema persiste, ejecuta:
   ```powershell
   python -c "from base_datos import BaseDatos; import sqlite3; conn = sqlite3.connect('registros/accesos.db'); cursor = conn.cursor(); cursor.execute('DELETE FROM vecinos WHERE LOWER(nombre) = \"matias\" AND activo = 0'); conn.commit(); print('Limpieza completada')"
   ```

### "No se detecta el rostro"
- Asegúrate de tener buena iluminación
- La cara debe estar centrada en la cámara
- No uses gafas oscuras ni cubras el rostro
- Intenta con una distancia de 50-100 cm de la cámara

### "Error al guardar en base de datos"
- Verifica permisos de escritura en la carpeta `registros/`
- Asegúrate de que no haya otro proceso usando `accesos.db`
- Reinicia el sistema y vuelve a intentar

---

## 💡 Consejos para Mejor Reconocimiento

1. **Foto de Registro:**
   - Usa buena iluminación (luz natural o LED blanca)
   - Rostro centrado y mirando a la cámara
   - Fondo simple sin distracciones
   - Expresión neutra

2. **Durante el Uso:**
   - El sistema reconocerá a Matias incluso con ligeros cambios
   - Funciona con gafas, gorras (sin cubrir el rostro), barba, etc.
   - La distancia óptima es 50-100 cm de la cámara

3. **Precisión:**
   - La tolerancia actual es `0.5` (equilibrada)
   - Si hay falsos positivos: reducir a `0.4`
   - Si no reconoce: aumentar a `0.6`
   - Ajustar en `config.json` → `tolerancia_reconocimiento`

---

## ✅ Checklist de Registro Exitoso

- [ ] Sistema iniciado correctamente
- [ ] Navegaste a "Gestión de Vecinos"
- [ ] Seleccionaste método de registro (cámara o archivo)
- [ ] Ingresaste el nombre "Matias"
- [ ] Capturaste/seleccionaste una foto clara
- [ ] Confirmaste el preview
- [ ] Viste el mensaje "registrado exitosamente"
- [ ] Verificaste que aparece en la lista de vecinos
- [ ] (Opcional) Probaste el reconocimiento facial

---

## 🎉 ¡Listo!

Una vez completados los pasos, "Matias" estará registrado como vecino y el sistema lo reconocerá automáticamente cada vez que pase frente a la cámara.

**Estado Final Esperado:**
```
✅ Matias registrado en base de datos
✅ Foto guardada en dataset/vecinos/Matias.jpg
✅ Encoding facial almacenado
✅ Sistema listo para reconocerlo
```

---

**Última actualización:** 30 de Octubre, 2025  
**Documento creado por:** GitHub Copilot
