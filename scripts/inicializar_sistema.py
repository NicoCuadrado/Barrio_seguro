"""
Script de Inicialización - Sistema Barrio Seguro
===============================================
Script para configurar el sistema y agregar datos de ejemplo.
"""

import os
import sys
import sqlite3
from datetime import datetime, timedelta
import logging

def crear_estructura_directorios():
    """Crea la estructura completa de directorios si no existe."""
    directorios = [
        "dataset",
        "dataset/vecinos", 
        "dataset/visitas",
        "registros"
    ]
    
    print("📁 Creando estructura de directorios...")
    for directorio in directorios:
        if not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f"✅ Creado: {directorio}")
        else:
            print(f"ℹ️  Ya existe: {directorio}")

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas."""
    print("🔍 Verificando dependencias...")
    
    dependencias = [
        ("cv2", "opencv-python"),
        ("face_recognition", "face_recognition"), 
        ("numpy", "numpy"),
        ("sqlite3", "incluido en Python")
    ]
    
    dependencias_faltantes = []
    
    for modulo, paquete in dependencias:
        try:
            __import__(modulo)
            print(f"✅ {modulo}: Disponible")
        except ImportError:
            print(f"❌ {modulo}: No disponible")
            dependencias_faltantes.append(paquete)
    
    if dependencias_faltantes:
        print(f"\n⚠️  Dependencias faltantes:")
        for dep in dependencias_faltantes:
            if dep != "incluido en Python":
                print(f"   pip install {dep}")
        return False
    
    print("✅ Todas las dependencias están disponibles")
    return True

def crear_base_datos_ejemplo():
    """Crea la base de datos con algunos datos de ejemplo."""
    print("💾 Inicializando base de datos...")
    
    try:
        from base_datos import BaseDatos
        db = BaseDatos()
        print("✅ Base de datos inicializada correctamente")
        
        # Agregar algunos registros de acceso de ejemplo
        registros_ejemplo = [
            ("Nicolas Cuadrado", "vecino", "entrada"),
            ("Maria Perez", "vecino", "entrada"),
            ("Visita_20241023", "visita", "entrada"),
            ("Nicolas Cuadrado", "vecino", "salida"),
            ("Visita_20241023", "visita", "salida"),
        ]
        
        print("📊 Agregando registros de ejemplo...")
        for nombre, tipo, evento in registros_ejemplo:
            db.registrar_acceso(nombre, tipo, evento)
        
        print("✅ Registros de ejemplo agregados")
        return True
        
    except ImportError:
        print("❌ No se pudo importar el módulo base_datos")
        return False
    except Exception as e:
        print(f"❌ Error al crear base de datos: {e}")
        return False

def crear_archivo_informacion():
    """Crea un archivo con información del proyecto."""
    info_contenido = """
=================================================================
               SISTEMA BARRIO SEGURO - INFORMACIÓN
=================================================================

📋 PRIMEROS PASOS:

1. 🚀 EJECUTAR EL SISTEMA:
   python main.py

2. 👤 REGISTRAR VECINOS:
   - Seleccionar opción 2 en el menú principal
   - Elegir "Registrar vecino (cámara)" o "desde archivo"
   - Seguir las instrucciones en pantalla

3. 🎥 INICIAR RECONOCIMIENTO:
   - Seleccionar opción 1 en el menú principal
   - Presionar 'q' para salir del reconocimiento
   - Presionar 'r' para registro rápido durante reconocimiento

📊 FUNCIONALIDADES DISPONIBLES:

• Reconocimiento facial en tiempo real
• Gestión completa de vecinos
• Control automático de visitas
• Análisis estadístico de accesos
• Configuración personalizable
• Exportación de reportes

⚙️ CONFIGURACIÓN:

• Archivo config.json para ajustes
• Tolerancia de reconocimiento ajustable
• Configuración de cámara personalizable
• Tiempo de visitas configurable

🔧 SOLUCIÓN DE PROBLEMAS:

• Si la cámara no funciona: verificar índice en config.json
• Si el reconocimiento es impreciso: ajustar tolerancia
• Para mejor rendimiento: modificar procesar_cada_n_frames

📁 ESTRUCTURA DE ARCHIVOS:

dataset/vecinos/     - Fotos de vecinos registrados
dataset/visitas/     - Fotos temporales de visitas  
registros/          - Base de datos y logs
config.json         - Configuración del sistema

=================================================================
Para soporte técnico, revisar el archivo README.md
=================================================================
    """.strip()
    
    with open("PRIMEROS_PASOS.txt", "w", encoding="utf-8") as f:
        f.write(info_contenido)
    
    print("✅ Archivo de información creado: PRIMEROS_PASOS.txt")

def verificar_camara():
    """Verifica si hay una cámara disponible."""
    print("📹 Verificando cámara...")
    
    try:
        import cv2
        
        # Probar cámaras en índices 0, 1, 2
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret and frame is not None:
                    print(f"✅ Cámara disponible en índice {i}")
                    return i
                    
        print("❌ No se encontró cámara disponible")
        return None
        
    except ImportError:
        print("❌ OpenCV no disponible para verificar cámara")
        return None

def main():
    """Función principal de inicialización."""
    print("🏠" + "="*60 + "🏠")
    print("🔧" + " "*20 + "INICIALIZACIÓN DEL SISTEMA" + " "*19 + "🔧")
    print("🏠" + "="*60 + "🏠")
    print()
    
    # Verificar dependencias
    if not verificar_dependencias():
        print("\n❌ No se puede continuar sin las dependencias necesarias.")
        print("📋 Instale las dependencias con: pip install -r requirements.txt")
        return False
    
    print()
    
    # Crear estructura de directorios
    crear_estructura_directorios()
    print()
    
    # Verificar cámara
    indice_camara = verificar_camara()
    if indice_camara is not None:
        # Actualizar config.json con el índice correcto
        try:
            import json
            with open("config.json", "r") as f:
                config = json.load(f)
            config["camara_index"] = indice_camara
            with open("config.json", "w") as f:
                json.dump(config, f, indent=4)
            print(f"✅ Configuración actualizada con cámara índice {indice_camara}")
        except:
            pass
    print()
    
    # Crear base de datos
    crear_base_datos_ejemplo()
    print()
    
    # Crear archivo de información
    crear_archivo_informacion()
    print()
    
    print("🎉" + "="*60 + "🎉")
    print("✅ SISTEMA INICIALIZADO CORRECTAMENTE")
    print("🎉" + "="*60 + "🎉")
    print()
    print("🚀 Para iniciar el sistema ejecute: python main.py")
    print("📖 Para más información consulte: PRIMEROS_PASOS.txt")
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            input("🎯 Presione ENTER para finalizar...")
        else:
            input("❌ Presione ENTER para salir...")
    except KeyboardInterrupt:
        print("\n\n🛑 Inicialización interrumpida por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante la inicialización: {e}")
        input("❌ Presione ENTER para salir...")