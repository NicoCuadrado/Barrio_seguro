"""
Utilidades para el Sistema Barrio Seguro
========================================
Módulo con funciones auxiliares, configuración de logs y constantes del sistema.
"""

import os
import logging
import cv2
import face_recognition as fr
import numpy as np
from datetime import datetime, timedelta
from typing import List, Tuple, Optional
import json


# ===== CONSTANTES DEL SISTEMA =====
TOLERANCIA_RECONOCIMIENTO = 0.5  # Tolerancia para el reconocimiento facial
TIEMPO_VISITA_MINUTOS = 30       # Tiempo para considerar la misma visita
CONFIANZA_MINIMA = 0.4           # Confianza mínima para reconocimiento
TAMAÑO_FRAME_PROCESAMIENTO = (320, 240)  # Tamaño para procesar frames rápidamente
FORMATO_FECHA_ARCHIVO = "%Y%m%d_%H%M%S"  # Formato para nombres de archivo

# Colores para rectángulos (BGR)
COLOR_VECINO = (0, 255, 0)      # Verde para vecinos reconocidos
COLOR_VISITA = (0, 0, 255)      # Rojo para visitas/desconocidos
COLOR_TEXTO = (255, 255, 255)   # Blanco para texto

# Configuración de logging
LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOG_FILE = 'registros/sistema.log'


def configurar_logging(nivel_log: str = "INFO"):
    """Configura el sistema de logging."""
    # Crear directorio de logs si no existe
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    
    # Configurar formato y handlers
    logging.basicConfig(
        level=getattr(logging, nivel_log.upper()),
        format=LOG_FORMAT,
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("Sistema de logging configurado")


def validar_imagen(ruta_imagen: str) -> bool:
    """Valida si un archivo es una imagen válida y puede ser cargada."""
    try:
        if not os.path.exists(ruta_imagen):
            return False
            
        # Intentar cargar la imagen
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            return False
            
        # Verificar que tenga contenido
        if imagen.size == 0:
            return False
            
        return True
        
    except Exception as e:
        logging.error(f"Error al validar imagen {ruta_imagen}: {e}")
        return False


def obtener_codificacion_facial(imagen) -> Optional[np.ndarray]:
    """Extrae la codificación facial de una imagen."""
    try:
        # Convertir a RGB
        rgb_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
        
        # Detectar caras
        ubicaciones_caras = fr.face_locations(rgb_imagen)
        
        if not ubicaciones_caras:
            logging.warning("No se detectaron caras en la imagen")
            return None
            
        # Obtener codificación de la primera cara
        codificaciones = fr.face_encodings(rgb_imagen, ubicaciones_caras)
        
        if not codificaciones:
            logging.warning("No se pudo codificar la cara detectada")
            return None
            
        return codificaciones[0]
        
    except Exception as e:
        logging.error(f"Error al obtener codificación facial: {e}")
        return None


def comparar_caras(codificacion_conocida: np.ndarray, 
                  codificacion_nueva: np.ndarray) -> Tuple[bool, float]:
    """Compara dos codificaciones faciales y retorna si coinciden y su distancia."""
    try:
        # Calcular distancia
        distancia = fr.face_distance([codificacion_conocida], codificacion_nueva)[0]
        
        # Determinar si es coincidencia
        es_coincidencia = distancia <= TOLERANCIA_RECONOCIMIENTO
        
        return es_coincidencia, distancia
        
    except Exception as e:
        logging.error(f"Error al comparar caras: {e}")
        return False, 1.0


def redimensionar_imagen(imagen, ancho_max: int = 800) -> np.ndarray:
    """Redimensiona una imagen manteniendo la proporción de aspecto."""
    try:
        alto, ancho = imagen.shape[:2]
        
        if ancho <= ancho_max:
            return imagen
            
        # Calcular nuevo tamaño manteniendo proporción
        factor = ancho_max / ancho
        nuevo_ancho = ancho_max
        nuevo_alto = int(alto * factor)
        
        return cv2.resize(imagen, (nuevo_ancho, nuevo_alto))
        
    except Exception as e:
        logging.error(f"Error al redimensionar imagen: {e}")
        return imagen


def generar_nombre_archivo_visita() -> str:
    """Genera un nombre único basado en timestamp para archivos de visita."""
    timestamp = datetime.now().strftime(FORMATO_FECHA_ARCHIVO)
    return f"visita_{timestamp}.jpg"


def limpiar_archivos_visitas_antiguas(directorio_visitas: str, dias_limite: int = 7):
    """Elimina archivos de visitas más antiguos que el límite especificado."""
    try:
        if not os.path.exists(directorio_visitas):
            return
            
        limite_tiempo = datetime.now() - timedelta(days=dias_limite)
        archivos_eliminados = 0
        
        for archivo in os.listdir(directorio_visitas):
            ruta_archivo = os.path.join(directorio_visitas, archivo)
            
            if os.path.isfile(ruta_archivo):
                # Obtener fecha de modificación
                tiempo_modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_archivo))
                
                if tiempo_modificacion < limite_tiempo:
                    os.remove(ruta_archivo)
                    archivos_eliminados += 1
                    
        if archivos_eliminados > 0:
            logging.info(f"Limpieza completada: {archivos_eliminados} archivos eliminados")
            
    except Exception as e:
        logging.error(f"Error en limpieza de archivos: {e}")


def dibujar_rectangulo_cara(imagen, ubicacion_cara: Tuple, nombre: str, 
                           es_vecino: bool = True, distancia: float = 0.0):
    """Dibuja un rectángulo alrededor de una cara con su nombre y datos."""
    try:
        top, right, bottom, left = ubicacion_cara
        
        # Seleccionar color según tipo de persona
        color = COLOR_VECINO if es_vecino else COLOR_VISITA
        
        # Dibujar rectángulo principal
        cv2.rectangle(imagen, (left, top), (right, bottom), color, 2)
        
        # Dibujar rectángulo para texto
        cv2.rectangle(imagen, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
        
        # Preparar texto
        if es_vecino:
            texto = f"{nombre}"
            texto_confianza = f"Dist: {distancia:.3f}"
        else:
            texto = "VISITA"
            texto_confianza = "DESCONOCIDO"
        
        # Escribir texto principal
        cv2.putText(imagen, texto, (left + 6, bottom - 6), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_TEXTO, 1)
        
        # Escribir información adicional si hay espacio
        if right - left > 100:  # Solo si el rectángulo es lo suficientemente ancho
            cv2.putText(imagen, texto_confianza, (left + 6, bottom - 20), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, COLOR_TEXTO, 1)
                       
    except Exception as e:
        logging.error(f"Error al dibujar rectángulo: {e}")


def cargar_configuracion(archivo_config: str = "config.json") -> dict:
    """Carga la configuración desde archivo JSON o crea una por defecto."""
    configuracion_default = {
        "tolerancia_reconocimiento": TOLERANCIA_RECONOCIMIENTO,
        "tiempo_visita_minutos": TIEMPO_VISITA_MINUTOS,
        "confianza_minima": CONFIANZA_MINIMA,
        "camara_index": 0,
        "fps_objetivo": 30,
        "resolucion_camara": [640, 480],
        "procesar_cada_n_frames": 3
    }
    
    try:
        if os.path.exists(archivo_config):
            with open(archivo_config, 'r', encoding='utf-8') as f:
                config_archivo = json.load(f)
                configuracion_default.update(config_archivo)
                logging.info("Configuración cargada desde archivo")
        else:
            # Crear archivo de configuración por defecto
            guardar_configuracion(configuracion_default, archivo_config)
            logging.info("Archivo de configuración creado con valores por defecto")
            
        return configuracion_default
        
    except Exception as e:
        logging.error(f"Error al cargar configuración: {e}")
        return configuracion_default


def guardar_configuracion(config: dict, archivo_config: str = "config.json"):
    """Guarda la configuración en archivo JSON."""
    try:
        with open(archivo_config, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
        logging.info("Configuración guardada exitosamente")
        
    except Exception as e:
        logging.error(f"Error al guardar configuración: {e}")


def verificar_camara(indice_camara: int = 0) -> bool:
    """Verifica si la cámara está disponible y funcionando."""
    try:
        captura = cv2.VideoCapture(indice_camara)
        if not captura.isOpened():
            return False
            
        # Intentar leer un frame
        ret, frame = captura.read()
        captura.release()
        
        return ret and frame is not None
        
    except Exception as e:
        logging.error(f"Error al verificar cámara: {e}")
        return False


def formatear_tiempo_transcurrido(inicio: datetime) -> str:
    """Formatea el tiempo transcurrido en formato legible (Xh Ym Zs)."""
    try:
        transcurrido = datetime.now() - inicio
        
        horas = int(transcurrido.total_seconds() // 3600)
        minutos = int((transcurrido.total_seconds() % 3600) // 60)
        segundos = int(transcurrido.total_seconds() % 60)
        
        if horas > 0:
            return f"{horas}h {minutos}m {segundos}s"
        elif minutos > 0:
            return f"{minutos}m {segundos}s"
        else:
            return f"{segundos}s"
            
    except Exception as e:
        logging.error(f"Error al formatear tiempo: {e}")
        return "0s"


def crear_directorio_si_no_existe(directorio: str):
    """Crea un directorio si no existe."""
    try:
        os.makedirs(directorio, exist_ok=True)
    except Exception as e:
        logging.error(f"Error al crear directorio {directorio}: {e}")


def obtener_info_sistema() -> dict:
    """Obtiene información del sistema para diagnóstico."""
    info = {
        "opencv_version": cv2.__version__,
        "python_version": os.sys.version,
        "timestamp": datetime.now().isoformat(),
        "camara_disponible": verificar_camara(0)
    }
    
    try:
        import face_recognition
        info["face_recognition_disponible"] = True
    except ImportError:
        info["face_recognition_disponible"] = False
    
    return info