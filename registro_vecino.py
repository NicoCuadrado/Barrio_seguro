"""
Módulo de Registro de Vecinos - Sistema Barrio Seguro
====================================================
Módulo para registrar nuevos vecinos con captura de foto y codificación facial.

Autor: Sistema Barrio Seguro
Fecha: 23/10/2025
"""

import cv2
import face_recognition as fr
import os
import logging
from datetime import datetime
from typing import Optional, Tuple
import numpy as np

from base_datos import BaseDatos
from utils import (
    obtener_codificacion_facial, validar_imagen, redimensionar_imagen,
    dibujar_rectangulo_cara, COLOR_VECINO, crear_directorio_si_no_existe
)


class RegistroVecino:
    """
    Clase para manejar el registro de nuevos vecinos.
    """
    
    def __init__(self, db: BaseDatos):
        """
        Inicializa el sistema de registro.
        
        Args:
            db (BaseDatos): Instancia de la base de datos
        """
        self.db = db
        self.directorio_vecinos = "dataset/vecinos"
        crear_directorio_si_no_existe(self.directorio_vecinos)
        
    def registrar_desde_camara(self, nombre: str) -> bool:
        """
        Registra un vecino capturando su foto desde la cámara.
        
        Args:
            nombre (str): Nombre del vecino
            
        Returns:
            bool: True si se registró exitosamente
        """
        try:
            logging.info(f"Iniciando registro desde cámara para: {nombre}")
            
            # Verificar si el vecino ya existe
            if self.db.buscar_vecino_por_nombre(nombre):
                logging.warning(f"El vecino {nombre} ya está registrado")
                print(f"❌ El vecino '{nombre}' ya está registrado en el sistema.")
                return False
            
            # Inicializar cámara
            captura = cv2.VideoCapture(0)
            if not captura.isOpened():
                logging.error("No se pudo abrir la cámara")
                print("❌ Error: No se pudo acceder a la cámara.")
                return False
            
            print(f"\n📸 REGISTRO DE VECINO: {nombre}")
            print("=" * 50)
            print("📋 Instrucciones:")
            print("   • Mire directamente a la cámara")
            print("   • Asegúrese de tener buena iluminación") 
            print("   • Presione ESPACIO para capturar la foto")
            print("   • Presione ESC para cancelar")
            print("=" * 50)
            
            foto_capturada = None
            codificacion_valida = None
            
            while True:
                ret, frame = captura.read()
                if not ret:
                    logging.error("Error al leer frame de la cámara")
                    break
                
                # Redimensionar para mostrar
                frame_mostrar = redimensionar_imagen(frame, 800)
                
                # Detectar caras en tiempo real para feedback
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                ubicaciones_caras = fr.face_locations(rgb_frame)
                
                # Dibujar rectángulos alrededor de las caras detectadas
                for ubicacion in ubicaciones_caras:
                    top, right, bottom, left = ubicacion
                    cv2.rectangle(frame_mostrar, (left, top), (right, bottom), COLOR_VECINO, 2)
                    cv2.putText(frame_mostrar, "CARA DETECTADA", (left, top - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_VECINO, 2)
                
                # Mostrar instrucciones en pantalla
                cv2.putText(frame_mostrar, f"Registrando: {nombre}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                cv2.putText(frame_mostrar, "ESPACIO: Capturar | ESC: Cancelar", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Mostrar estado de detección
                if ubicaciones_caras:
                    cv2.putText(frame_mostrar, f"Caras detectadas: {len(ubicaciones_caras)}", (10, 90),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                else:
                    cv2.putText(frame_mostrar, "Sin caras detectadas", (10, 90),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
                
                cv2.imshow("Registro de Vecino", frame_mostrar)
                
                tecla = cv2.waitKey(1) & 0xFF
                
                # Capturar foto con ESPACIO
                if tecla == ord(' '):
                    if ubicaciones_caras:
                        if len(ubicaciones_caras) == 1:
                            foto_capturada = frame.copy()
                            print("✅ Foto capturada exitosamente")
                            break
                        else:
                            print("⚠️  Se detectaron múltiples caras. Asegúrese de que solo haya una persona.")
                    else:
                        print("⚠️  No se detectó ninguna cara. Intente nuevamente.")
                
                # Cancelar con ESC
                elif tecla == 27:  # ESC
                    print("❌ Registro cancelado por el usuario")
                    captura.release()
                    cv2.destroyAllWindows()
                    return False
            
            captura.release()
            cv2.destroyAllWindows()
            
            if foto_capturada is None:
                logging.error("No se capturó ninguna foto")
                return False
            
            # Procesar la foto capturada
            return self._procesar_y_guardar_vecino(nombre, foto_capturada)
            
        except Exception as e:
            logging.error(f"Error en registro desde cámara: {e}")
            print(f"❌ Error durante el registro: {e}")
            return False
    
    def registrar_desde_archivo(self, nombre: str, ruta_imagen: str) -> bool:
        """
        Registra un vecino desde un archivo de imagen.
        
        Args:
            nombre (str): Nombre del vecino
            ruta_imagen (str): Ruta al archivo de imagen
            
        Returns:
            bool: True si se registró exitosamente
        """
        try:
            logging.info(f"Iniciando registro desde archivo para: {nombre}")
            
            # Verificar si el vecino ya existe
            if self.db.buscar_vecino_por_nombre(nombre):
                logging.warning(f"El vecino {nombre} ya está registrado")
                print(f"❌ El vecino '{nombre}' ya está registrado en el sistema.")
                return False
            
            # Validar archivo de imagen
            if not validar_imagen(ruta_imagen):
                logging.error(f"Archivo de imagen inválido: {ruta_imagen}")
                print(f"❌ El archivo '{ruta_imagen}' no es una imagen válida.")
                return False
            
            # Cargar imagen
            imagen = cv2.imread(ruta_imagen)
            if imagen is None:
                logging.error(f"No se pudo cargar la imagen: {ruta_imagen}")
                print(f"❌ No se pudo cargar la imagen: {ruta_imagen}")
                return False
            
            print(f"\n📁 REGISTRO DESDE ARCHIVO: {nombre}")
            print("=" * 50)
            
            # Procesar la imagen
            return self._procesar_y_guardar_vecino(nombre, imagen, ruta_imagen)
            
        except Exception as e:
            logging.error(f"Error en registro desde archivo: {e}")
            print(f"❌ Error durante el registro: {e}")
            return False
    
    def _procesar_y_guardar_vecino(self, nombre: str, imagen: np.ndarray, 
                                  ruta_origen: str = None) -> bool:
        """
        Procesa la imagen y guarda el vecino en la base de datos.
        
        Args:
            nombre (str): Nombre del vecino
            imagen (np.ndarray): Imagen del vecino
            ruta_origen (str): Ruta de origen si viene de archivo
            
        Returns:
            bool: True si se procesó exitosamente
        """
        try:
            print("🔍 Procesando imagen...")
            
            # Obtener codificación facial
            codificacion = obtener_codificacion_facial(imagen)
            if codificacion is None:
                print("❌ No se pudo detectar una cara en la imagen.")
                return False
            
            print("✅ Cara detectada y codificada exitosamente")
            
            # Generar nombre de archivo
            nombre_archivo = f"{nombre.lower().replace(' ', '_')}.jpg"
            ruta_destino = os.path.join(self.directorio_vecinos, nombre_archivo)
            
            # Guardar imagen en el directorio de vecinos
            if ruta_origen and os.path.exists(ruta_origen):
                # Si viene de archivo, copiarlo
                import shutil
                shutil.copy2(ruta_origen, ruta_destino)
                print(f"📋 Imagen copiada a: {ruta_destino}")
            else:
                # Si viene de cámara, guardar la captura
                cv2.imwrite(ruta_destino, imagen)
                print(f"💾 Imagen guardada en: {ruta_destino}")
            
            # Registrar en base de datos
            if self.db.registrar_vecino(nombre, ruta_destino, codificacion):
                print("=" * 50)
                print(f"🎉 ¡VECINO REGISTRADO EXITOSAMENTE!")
                print(f"   👤 Nombre: {nombre}")
                print(f"   📁 Imagen: {ruta_destino}")
                print(f"   📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                print("=" * 50)
                
                logging.info(f"Vecino {nombre} registrado exitosamente")
                return True
            else:
                print("❌ Error al guardar en la base de datos")
                # Eliminar archivo si falló el registro en BD
                if os.path.exists(ruta_destino):
                    os.remove(ruta_destino)
                return False
                
        except Exception as e:
            logging.error(f"Error al procesar vecino: {e}")
            print(f"❌ Error al procesar vecino: {e}")
            return False
    
    def mostrar_preview_imagen(self, ruta_imagen: str) -> bool:
        """
        Muestra un preview de la imagen antes de registrar.
        
        Args:
            ruta_imagen (str): Ruta de la imagen
            
        Returns:
            bool: True si el usuario confirma el registro
        """
        try:
            if not validar_imagen(ruta_imagen):
                print(f"❌ Imagen inválida: {ruta_imagen}")
                return False
            
            imagen = cv2.imread(ruta_imagen)
            if imagen is None:
                return False
            
            # Redimensionar para mostrar
            imagen_mostrar = redimensionar_imagen(imagen, 600)
            
            # Detectar caras para preview
            rgb_imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)
            ubicaciones_caras = fr.face_locations(rgb_imagen)
            
            # Dibujar rectángulos alrededor de caras detectadas
            for ubicacion in ubicaciones_caras:
                top, right, bottom, left = ubicacion
                cv2.rectangle(imagen_mostrar, (left, top), (right, bottom), COLOR_VECINO, 2)
                cv2.putText(imagen_mostrar, "CARA DETECTADA", (left, top - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, COLOR_VECINO, 2)
            
            # Mostrar información
            cv2.putText(imagen_mostrar, f"Caras detectadas: {len(ubicaciones_caras)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(imagen_mostrar, "ENTER: Continuar | ESC: Cancelar", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow("Preview - Imagen de Vecino", imagen_mostrar)
            
            print(f"\n📋 PREVIEW DE IMAGEN")
            print("=" * 30)
            print(f"📁 Archivo: {ruta_imagen}")
            print(f"👥 Caras detectadas: {len(ubicaciones_caras)}")
            
            if len(ubicaciones_caras) == 0:
                print("⚠️  ADVERTENCIA: No se detectaron caras en la imagen")
            elif len(ubicaciones_caras) > 1:
                print("⚠️  ADVERTENCIA: Se detectaron múltiples caras")
            else:
                print("✅ Una cara detectada - Imagen válida")
            
            print("\n🎯 Presione ENTER para continuar o ESC para cancelar")
            
            while True:
                tecla = cv2.waitKey(0) & 0xFF
                if tecla == 13:  # ENTER
                    cv2.destroyAllWindows()
                    return True
                elif tecla == 27:  # ESC
                    cv2.destroyAllWindows()
                    return False
                    
        except Exception as e:
            logging.error(f"Error en preview: {e}")
            return False
    
    def listar_vecinos_registrados(self):
        """
        Lista todos los vecinos registrados en el sistema.
        """
        try:
            vecinos = self.db.obtener_vecinos_activos()
            
            print(f"\n👥 VECINOS REGISTRADOS EN EL SISTEMA")
            print("=" * 60)
            
            if not vecinos:
                print("📝 No hay vecinos registrados en el sistema.")
                return
            
            print(f"📊 Total de vecinos: {len(vecinos)}")
            print("-" * 60)
            
            for i, (id_vecino, nombre, _) in enumerate(vecinos, 1):
                # Obtener información adicional del vecino
                info_vecino = self.db.buscar_vecino_por_nombre(nombre)
                if info_vecino:
                    fecha_registro = info_vecino[3]  # fecha_registro
                    print(f"{i:2d}. 👤 {nombre}")
                    print(f"     📅 Registrado: {fecha_registro}")
                    print(f"     🆔 ID: {id_vecino}")
                    print("-" * 40)
            
            print("=" * 60)
            
        except Exception as e:
            logging.error(f"Error al listar vecinos: {e}")
            print(f"❌ Error al obtener lista de vecinos: {e}")
    
    def eliminar_vecino(self, nombre: str) -> bool:
        """
        Elimina un vecino del sistema.
        
        Args:
            nombre (str): Nombre del vecino a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            # Verificar si el vecino existe
            vecino = self.db.buscar_vecino_por_nombre(nombre)
            if not vecino:
                print(f"❌ El vecino '{nombre}' no existe en el sistema.")
                return False
            
            print(f"\n⚠️  ELIMINAR VECINO: {nombre}")
            print("=" * 40)
            print("🚨 Esta acción desactivará al vecino del sistema.")
            print("🚨 Los registros de acceso se mantendrán.")
            
            confirmacion = input("\n❓ ¿Está seguro? (s/N): ").strip().lower()
            
            if confirmacion == 's':
                if self.db.eliminar_vecino(nombre):
                    print(f"✅ Vecino '{nombre}' eliminado del sistema.")
                    logging.info(f"Vecino {nombre} eliminado")
                    return True
                else:
                    print(f"❌ Error al eliminar vecino '{nombre}'.")
                    return False
            else:
                print("❌ Eliminación cancelada.")
                return False
                
        except Exception as e:
            logging.error(f"Error al eliminar vecino: {e}")
            print(f"❌ Error al eliminar vecino: {e}")
            return False


def menu_registro_interactivo():
    """
    Menú interactivo para registro de vecinos.
    """
    try:
        # Configurar logging
        from utils import configurar_logging
        configurar_logging()
        
        print("\n🏠 SISTEMA DE REGISTRO DE VECINOS")
        print("=" * 50)
        
        # Inicializar sistema
        db = BaseDatos()
        registro = RegistroVecino(db)
        
        while True:
            print(f"\n📋 MENÚ DE REGISTRO")
            print("-" * 30)
            print("1. 📸 Registrar desde cámara")
            print("2. 📁 Registrar desde archivo")
            print("3. 👥 Listar vecinos registrados")
            print("4. 🗑️  Eliminar vecino")
            print("5. 🚪 Salir")
            
            opcion = input("\n🎯 Seleccione una opción (1-5): ").strip()
            
            if opcion == '1':
                nombre = input("👤 Ingrese el nombre del vecino: ").strip()
                if nombre:
                    registro.registrar_desde_camara(nombre)
                else:
                    print("❌ Debe ingresar un nombre válido.")
            
            elif opcion == '2':
                nombre = input("👤 Ingrese el nombre del vecino: ").strip()
                if not nombre:
                    print("❌ Debe ingresar un nombre válido.")
                    continue
                    
                ruta = input("📁 Ingrese la ruta de la imagen: ").strip()
                if not ruta:
                    print("❌ Debe ingresar una ruta válida.")
                    continue
                
                # Mostrar preview antes de registrar
                if registro.mostrar_preview_imagen(ruta):
                    registro.registrar_desde_archivo(nombre, ruta)
                else:
                    print("❌ Registro cancelado.")
            
            elif opcion == '3':
                registro.listar_vecinos_registrados()
            
            elif opcion == '4':
                nombre = input("👤 Ingrese el nombre del vecino a eliminar: ").strip()
                if nombre:
                    registro.eliminar_vecino(nombre)
                else:
                    print("❌ Debe ingresar un nombre válido.")
            
            elif opcion == '5':
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida. Intente nuevamente.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrumpido por el usuario.")
    except Exception as e:
        logging.error(f"Error en menú de registro: {e}")
        print(f"❌ Error en el sistema: {e}")


if __name__ == "__main__":
    menu_registro_interactivo()