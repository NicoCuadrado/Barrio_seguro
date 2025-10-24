"""
Módulo de Reconocimiento Facial - Sistema Barrio Seguro
=======================================================
Motor principal de reconocimiento facial en tiempo real con manejo de visitas.

Autor: Sistema Barrio Seguro
Fecha: 23/10/2025
"""

import cv2
import face_recognition as fr
import os
import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Optional, Dict, Any
import numpy as np
import time

from base_datos import BaseDatos
from utils import (
    obtener_codificacion_facial, comparar_caras, dibujar_rectangulo_cara,
    generar_nombre_archivo_visita, configurar_logging, cargar_configuracion,
    redimensionar_imagen, formatear_tiempo_transcurrido, COLOR_VECINO, COLOR_VISITA,
    TIEMPO_VISITA_MINUTOS, crear_directorio_si_no_existe
)


class SistemaReconocimiento:
    """
    Sistema principal de reconocimiento facial en tiempo real.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Inicializa el sistema de reconocimiento.
        
        Args:
            config (Dict): Configuración del sistema
        """
        self.config = config or cargar_configuracion()
        self.db = BaseDatos()
        
        # Directorios
        self.directorio_visitas = "dataset/visitas"
        crear_directorio_si_no_existe(self.directorio_visitas)
        
        # Datos de vecinos precargados
        self.vecinos_conocidos = []
        self.nombres_vecinos = []
        self.encodings_vecinos = []
        
        # Control de visitas temporales
        self.visitas_activas = {}  # {encoding_hash: {info_visita}}
        self.ultimo_reconocimiento = {}  # {nombre: timestamp}
        
        # Configuración de cámara
        self.camara = None
        self.fps_objetivo = self.config.get('fps_objetivo', 30)
        self.procesar_cada_n_frames = self.config.get('procesar_cada_n_frames', 3)
        self.contador_frames = 0
        
        # Control de tiempo
        self.inicio_sesion = datetime.now()
        self.stats_sesion = {
            'vecinos_detectados': set(),
            'visitas_registradas': 0,
            'total_detecciones': 0
        }
        
        logging.info("Sistema de reconocimiento inicializado")
    
    def cargar_vecinos_conocidos(self) -> bool:
        """
        Precarga todos los vecinos conocidos para acelerar el reconocimiento.
        
        Returns:
            bool: True si se cargaron exitosamente
        """
        try:
            print("🔄 Cargando vecinos conocidos...")
            
            self.vecinos_conocidos = self.db.obtener_vecinos_activos()
            self.nombres_vecinos = []
            self.encodings_vecinos = []
            
            for id_vecino, nombre, encoding in self.vecinos_conocidos:
                self.nombres_vecinos.append(nombre)
                self.encodings_vecinos.append(encoding)
            
            print(f"✅ {len(self.vecinos_conocidos)} vecinos cargados exitosamente")
            logging.info(f"Cargados {len(self.vecinos_conocidos)} vecinos conocidos")
            return True
            
        except Exception as e:
            logging.error(f"Error al cargar vecinos: {e}")
            print(f"❌ Error al cargar vecinos: {e}")
            return False
    
    def cargar_visitas_temporales(self):
        """
        Carga las visitas temporales activas desde la base de datos.
        """
        try:
            visitas_db = self.db.obtener_visitas_temporales_activas()
            
            for id_visita, nombre_archivo, encoding, fecha_entrada in visitas_db:
                # Calcular tiempo transcurrido
                fecha_entrada_dt = datetime.fromisoformat(fecha_entrada.replace('Z', '+00:00'))
                tiempo_transcurrido = datetime.now() - fecha_entrada_dt
                
                # Si la visita es muy antigua, desactivarla
                if tiempo_transcurrido.total_seconds() > (TIEMPO_VISITA_MINUTOS * 60):
                    self.db.desactivar_visita_temporal(id_visita)
                    # Eliminar archivo de imagen
                    ruta_imagen = os.path.join(self.directorio_visitas, nombre_archivo)
                    if os.path.exists(ruta_imagen):
                        os.remove(ruta_imagen)
                else:
                    # Mantener visita activa
                    encoding_hash = hash(encoding.tobytes())
                    self.visitas_activas[encoding_hash] = {
                        'id': id_visita,
                        'nombre_archivo': nombre_archivo,
                        'encoding': encoding,
                        'fecha_entrada': fecha_entrada_dt,
                        'ultima_deteccion': fecha_entrada_dt
                    }
                    
            logging.info(f"Cargadas {len(self.visitas_activas)} visitas temporales")
            
        except Exception as e:
            logging.error(f"Error al cargar visitas temporales: {e}")
    
    def inicializar_camara(self) -> bool:
        """
        Inicializa y configura la cámara.
        
        Returns:
            bool: True si se inicializó correctamente
        """
        try:
            indice_camara = self.config.get('camara_index', 0)
            print(f"📹 Inicializando cámara (índice: {indice_camara})...")
            
            self.camara = cv2.VideoCapture(indice_camara)
            
            if not self.camara.isOpened():
                logging.error(f"No se pudo abrir la cámara {indice_camara}")
                return False
            
            # Configurar resolución
            resolucion = self.config.get('resolucion_camara', [640, 480])
            self.camara.set(cv2.CAP_PROP_FRAME_WIDTH, resolucion[0])
            self.camara.set(cv2.CAP_PROP_FRAME_HEIGHT, resolucion[1])
            
            # Configurar FPS
            self.camara.set(cv2.CAP_PROP_FPS, self.fps_objetivo)
            
            print("✅ Cámara inicializada correctamente")
            logging.info("Cámara inicializada exitosamente")
            return True
            
        except Exception as e:
            logging.error(f"Error al inicializar cámara: {e}")
            print(f"❌ Error al inicializar cámara: {e}")
            return False
    
    def reconocer_persona(self, encoding_cara) -> Tuple[Optional[str], bool, float]:
        """
        Reconoce una persona comparando con encodings conocidos.
        
        Args:
            encoding_cara: Encoding facial a comparar
            
        Returns:
            Tuple[Optional[str], bool, float]: (nombre, es_vecino, distancia)
        """
        try:
            # Primero verificar vecinos conocidos
            if self.encodings_vecinos:
                distancias = fr.face_distance(self.encodings_vecinos, encoding_cara)
                mejor_coincidencia_idx = np.argmin(distancias)
                distancia_minima = distancias[mejor_coincidencia_idx]
                
                tolerancia = self.config.get('tolerancia_reconocimiento', 0.5)
                
                if distancia_minima <= tolerancia:
                    nombre = self.nombres_vecinos[mejor_coincidencia_idx]
                    return nombre, True, distancia_minima
            
            # Verificar visitas temporales
            encoding_hash = hash(encoding_cara.tobytes())
            
            for hash_visita, info_visita in self.visitas_activas.items():
                es_coincidencia, distancia = comparar_caras(
                    info_visita['encoding'], encoding_cara
                )
                
                if es_coincidencia:
                    # Actualizar última detección
                    info_visita['ultima_deteccion'] = datetime.now()
                    nombre_visita = f"Visita_{info_visita['nombre_archivo'][:8]}"
                    return nombre_visita, False, distancia
            
            # No se reconoció la persona
            return None, False, 1.0
            
        except Exception as e:
            logging.error(f"Error en reconocimiento: {e}")
            return None, False, 1.0
    
    def procesar_nueva_visita(self, encoding_cara, frame, ubicacion_cara) -> str:
        """
        Procesa una nueva visita no reconocida.
        
        Args:
            encoding_cara: Encoding facial de la visita
            frame: Frame actual de la cámara
            ubicacion_cara: Ubicación de la cara en el frame
            
        Returns:
            str: Nombre asignado a la visita
        """
        try:
            # Generar nombre único para la visita
            nombre_archivo = generar_nombre_archivo_visita()
            ruta_imagen = os.path.join(self.directorio_visitas, nombre_archivo)
            
            # Extraer la región de la cara
            top, right, bottom, left = ubicacion_cara
            cara_recortada = frame[top:bottom, left:right]
            
            # Guardar imagen de la visita
            cv2.imwrite(ruta_imagen, cara_recortada)
            
            # Registrar en base de datos
            self.db.registrar_visita_temporal(nombre_archivo, encoding_cara)
            
            # Agregar a visitas activas
            encoding_hash = hash(encoding_cara.tobytes())
            self.visitas_activas[encoding_hash] = {
                'nombre_archivo': nombre_archivo,
                'encoding': encoding_cara,
                'fecha_entrada': datetime.now(),
                'ultima_deteccion': datetime.now()
            }
            
            # Registrar acceso
            nombre_visita = f"Visita_{nombre_archivo[:8]}"
            self.db.registrar_acceso(nombre_visita, "visita", "entrada", ruta_imagen)
            
            self.stats_sesion['visitas_registradas'] += 1
            
            logging.info(f"Nueva visita registrada: {nombre_visita}")
            print(f"👥 Nueva visita detectada: {nombre_visita}")
            
            return nombre_visita
            
        except Exception as e:
            logging.error(f"Error al procesar nueva visita: {e}")
            return "Visita_Error"
    
    def actualizar_ultimo_acceso(self, nombre: str, es_vecino: bool):
        """
        Actualiza el registro del último acceso de una persona.
        
        Args:
            nombre (str): Nombre de la persona
            es_vecino (bool): True si es vecino, False si es visita
        """
        try:
            ahora = datetime.now()
            
            # Verificar si ya se registró recientemente (evitar spam)
            if nombre in self.ultimo_reconocimiento:
                tiempo_transcurrido = ahora - self.ultimo_reconocimiento[nombre]
                if tiempo_transcurrido.total_seconds() < 30:  # 30 segundos de cooldown
                    return
            
            # Registrar acceso
            tipo_persona = "vecino" if es_vecino else "visita"
            self.db.registrar_acceso(nombre, tipo_persona, "entrada")
            
            # Actualizar timestamp
            self.ultimo_reconocimiento[nombre] = ahora
            
            if es_vecino:
                self.stats_sesion['vecinos_detectados'].add(nombre)
            
            logging.info(f"Acceso registrado: {nombre} ({tipo_persona})")
            
        except Exception as e:
            logging.error(f"Error al actualizar acceso: {e}")
    
    def limpiar_visitas_expiradas(self):
        """
        Limpia visitas que han excedido el tiempo límite.
        """
        try:
            ahora = datetime.now()
            visitas_a_eliminar = []
            
            for hash_visita, info_visita in self.visitas_activas.items():
                tiempo_transcurrido = ahora - info_visita['ultima_deteccion']
                
                if tiempo_transcurrido.total_seconds() > (TIEMPO_VISITA_MINUTOS * 60):
                    visitas_a_eliminar.append(hash_visita)
                    
                    # Registrar salida
                    nombre_visita = f"Visita_{info_visita['nombre_archivo'][:8]}"
                    self.db.registrar_acceso(nombre_visita, "visita", "salida")
                    
                    # Desactivar en BD
                    if 'id' in info_visita:
                        self.db.desactivar_visita_temporal(info_visita['id'])
                    
                    # Eliminar archivo
                    ruta_imagen = os.path.join(self.directorio_visitas, info_visita['nombre_archivo'])
                    if os.path.exists(ruta_imagen):
                        os.remove(ruta_imagen)
                    
                    logging.info(f"Visita expirada eliminada: {nombre_visita}")
            
            # Eliminar de memoria
            for hash_visita in visitas_a_eliminar:
                del self.visitas_activas[hash_visita]
                
        except Exception as e:
            logging.error(f"Error al limpiar visitas: {e}")
    
    def mostrar_estadisticas_sesion(self, frame):
        """
        Muestra estadísticas de la sesión actual en el frame.
        
        Args:
            frame: Frame donde mostrar las estadísticas
        """
        try:
            # Información de sesión
            tiempo_sesion = formatear_tiempo_transcurrido(self.inicio_sesion)
            
            # Texto de estadísticas
            stats_text = [
                f"Tiempo sesion: {tiempo_sesion}",
                f"Vecinos detectados: {len(self.stats_sesion['vecinos_detectados'])}",
                f"Visitas activas: {len(self.visitas_activas)}",
                f"Total registros: {self.stats_sesion['visitas_registradas']}"
            ]
            
            # Mostrar estadísticas
            y_offset = 30
            for i, texto in enumerate(stats_text):
                cv2.putText(frame, texto, (10, y_offset + i * 25),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
            
            # Mostrar controles
            cv2.putText(frame, "Presione 'q' para salir", (10, frame.shape[0] - 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
            cv2.putText(frame, "Presione 'r' para registro", (10, frame.shape[0] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 1)
                       
        except Exception as e:
            logging.error(f"Error al mostrar estadísticas: {e}")
    
    def iniciar_reconocimiento(self):
        """
        Inicia el sistema de reconocimiento en tiempo real.
        """
        try:
            print("\n🚀 INICIANDO SISTEMA DE RECONOCIMIENTO")
            print("=" * 60)
            
            # Cargar datos
            if not self.cargar_vecinos_conocidos():
                print("❌ Error al cargar vecinos. Abortando.")
                return
            
            self.cargar_visitas_temporales()
            
            # Inicializar cámara
            if not self.inicializar_camara():
                print("❌ Error al inicializar cámara. Abortando.")
                return
            
            print("\n📋 CONTROLES:")
            print("   • 'q' - Salir del sistema")
            print("   • 'r' - Modo registro de vecino")
            print("   • 'c' - Limpiar visitas expiradas manualmente")
            print("=" * 60)
            print("🎯 Sistema activo - Reconocimiento en tiempo real")
            
            ultimo_cleanup = datetime.now()
            
            while True:
                ret, frame = self.camara.read()
                if not ret:
                    logging.error("Error al leer frame de la cámara")
                    break
                
                # Procesar solo cada N frames para mejorar rendimiento
                self.contador_frames += 1
                procesar_frame = (self.contador_frames % self.procesar_cada_n_frames) == 0
                
                if procesar_frame:
                    # Redimensionar frame para procesamiento más rápido
                    frame_pequeno = cv2.resize(frame, (320, 240))
                    rgb_frame_pequeno = cv2.cvtColor(frame_pequeno, cv2.COLOR_BGR2RGB)
                    
                    # Detectar caras
                    ubicaciones_caras = fr.face_locations(rgb_frame_pequeno)
                    encodings_caras = fr.face_encodings(rgb_frame_pequeno, ubicaciones_caras)
                    
                    # Escalar ubicaciones de vuelta al tamaño original
                    factor_escala_x = frame.shape[1] / 320
                    factor_escala_y = frame.shape[0] / 240
                    
                    for (top, right, bottom, left), encoding_cara in zip(ubicaciones_caras, encodings_caras):
                        # Escalar coordenadas
                        top = int(top * factor_escala_y)
                        right = int(right * factor_escala_x)
                        bottom = int(bottom * factor_escala_y)
                        left = int(left * factor_escala_x)
                        
                        ubicacion_escalada = (top, right, bottom, left)
                        
                        # Reconocer persona
                        nombre, es_vecino, distancia = self.reconocer_persona(encoding_cara)
                        
                        if nombre:
                            # Persona reconocida
                            self.actualizar_ultimo_acceso(nombre, es_vecino)
                            self.stats_sesion['total_detecciones'] += 1
                        else:
                            # Nueva visita
                            nombre = self.procesar_nueva_visita(encoding_cara, frame, ubicacion_escalada)
                            es_vecino = False
                            self.stats_sesion['total_detecciones'] += 1
                        
                        # Dibujar rectángulo y etiqueta
                        dibujar_rectangulo_cara(frame, ubicacion_escalada, nombre, es_vecino, distancia)
                
                # Mostrar estadísticas
                self.mostrar_estadisticas_sesion(frame)
                
                # Mostrar frame
                cv2.imshow("Sistema Barrio Seguro - Reconocimiento", frame)
                
                # Limpiar visitas expiradas cada 2 minutos
                if (datetime.now() - ultimo_cleanup).total_seconds() > 120:
                    self.limpiar_visitas_expiradas()
                    ultimo_cleanup = datetime.now()
                
                # Manejar teclas
                tecla = cv2.waitKey(1) & 0xFF
                
                if tecla == ord('q'):
                    print("\n🛑 Deteniendo sistema...")
                    break
                elif tecla == ord('r'):
                    print("\n📝 Iniciando modo registro...")
                    self.modo_registro_rapido()
                elif tecla == ord('c'):
                    print("\n🧹 Limpiando visitas expiradas...")
                    self.limpiar_visitas_expiradas()
            
            self.finalizar_sistema()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Sistema interrumpido por el usuario")
            self.finalizar_sistema()
        except Exception as e:
            logging.error(f"Error en reconocimiento: {e}")
            print(f"❌ Error crítico: {e}")
            self.finalizar_sistema()
    
    def modo_registro_rapido(self):
        """
        Modo rápido de registro de vecino durante el reconocimiento.
        """
        try:
            cv2.destroyAllWindows()
            
            nombre = input("\n👤 Ingrese el nombre del vecino para registro rápido: ").strip()
            if not nombre:
                print("❌ Nombre inválido. Regresando al reconocimiento.")
                return
            
            from registro_vecino import RegistroVecino
            registro = RegistroVecino(self.db)
            
            if registro.registrar_desde_camara(nombre):
                print("✅ Vecino registrado. Recargando sistema...")
                self.cargar_vecinos_conocidos()
            else:
                print("❌ Error en el registro.")
            
            print("🔄 Regresando al reconocimiento en 3 segundos...")
            time.sleep(3)
            
        except Exception as e:
            logging.error(f"Error en registro rápido: {e}")
            print(f"❌ Error en registro rápido: {e}")
    
    def finalizar_sistema(self):
        """
        Finaliza el sistema de reconocimiento de forma segura.
        """
        try:
            if self.camara:
                self.camara.release()
            
            cv2.destroyAllWindows()
            
            # Mostrar resumen de sesión
            print("\n📊 RESUMEN DE SESIÓN")
            print("=" * 40)
            print(f"⏱️  Duración: {formatear_tiempo_transcurrido(self.inicio_sesion)}")
            print(f"👥 Vecinos únicos detectados: {len(self.stats_sesion['vecinos_detectados'])}")
            print(f"🚶 Visitas registradas: {self.stats_sesion['visitas_registradas']}")
            print(f"🔍 Total detecciones: {self.stats_sesion['total_detecciones']}")
            print("=" * 40)
            print("👋 ¡Sistema finalizado exitosamente!")
            
            logging.info("Sistema de reconocimiento finalizado")
            
        except Exception as e:
            logging.error(f"Error al finalizar sistema: {e}")


def main():
    """
    Función principal para ejecutar el sistema de reconocimiento.
    """
    try:
        # Configurar logging
        configurar_logging()
        
        print("🏠 SISTEMA BARRIO SEGURO")
        print("🔒 Control de Acceso por Reconocimiento Facial")
        print("=" * 60)
        
        # Cargar configuración
        config = cargar_configuracion()
        
        # Inicializar sistema
        sistema = SistemaReconocimiento(config)
        
        # Iniciar reconocimiento
        sistema.iniciar_reconocimiento()
        
    except Exception as e:
        logging.error(f"Error en función principal: {e}")
        print(f"❌ Error crítico en el sistema: {e}")


if __name__ == "__main__":
    main()