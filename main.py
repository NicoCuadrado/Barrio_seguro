"""
Sistema Barrio Seguro - Archivo Principal
=========================================
Sistema completo de reconocimiento facial para control de acceso a barrio privado.

Autor: Sistema Barrio Seguro
Fecha: 23/10/2025
Versión: 1.0

Características principales:
- Reconocimiento facial en tiempo real
- Registro de vecinos con captura desde cámara
- Control de visitas temporales
- Análisis estadístico de accesos
- Base de datos SQLite integrada
- Interfaz de usuario intuitiva
"""

import os
import sys
import logging
import sqlite3
from datetime import datetime
from typing import Optional

# Importar módulos del sistema
try:
    from utils import configurar_logging, cargar_configuracion, obtener_info_sistema, verificar_camara
    from base_datos import BaseDatos
    from reconocimiento import SistemaReconocimiento
    from registro_vecino import RegistroVecino, menu_registro_interactivo
    from analisis_registros import AnalisisRegistros, menu_analisis
except ImportError as e:
    print(f"❌ Error al importar módulos: {e}")
    print("🔧 Asegúrese de que todos los archivos estén en el directorio correcto.")
    sys.exit(1)


class SistemaBarrioSeguro:
    """
    Clase principal que coordina todos los módulos del sistema.
    """
    
    def __init__(self):
        """
        Inicializa el sistema principal.
        """
        self.version = "1.0"
        self.db = None
        self.config = None
        self.sistema_reconocimiento = None
        
        # Inicializar logging
        configurar_logging()
        logging.info("Iniciando Sistema Barrio Seguro")
        
    def inicializar_sistema(self) -> bool:
        """
        Inicializa todos los componentes del sistema.
        
        Returns:
            bool: True si se inicializó correctamente
        """
        try:
            print("🔧 Inicializando sistema...")
            
            # Cargar configuración
            self.config = cargar_configuracion()
            print("✅ Configuración cargada")
            
            # Inicializar base de datos
            self.db = BaseDatos()
            print("✅ Base de datos inicializada")
            
            # Verificar cámara
            if verificar_camara(self.config.get('camara_index', 0)):
                print("✅ Cámara disponible")
            else:
                print("⚠️  Advertencia: Cámara no disponible")
            
            return True
            
        except Exception as e:
            logging.error(f"Error al inicializar sistema: {e}")
            print(f"❌ Error al inicializar: {e}")
            return False
    
    def mostrar_bienvenida(self):
        """
        Muestra la pantalla de bienvenida del sistema.
        """
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpiar pantalla
        
        print("🏠" + "="*78 + "🏠")
        print("🔒" + " "*30 + "BARRIO SEGURO" + " "*33 + "🔒")
        print("👥" + " "*25 + "Sistema de Control de Acceso" + " "*25 + "👥")
        print("📹" + " "*25 + "Reconocimiento Facial v" + self.version + " "*24 + "📹")
        print("🏠" + "="*78 + "🏠")
        print()
        print("🎯 Funcionalidades principales:")
        print("   • 📸 Reconocimiento facial en tiempo real")
        print("   • 👤 Registro de vecinos del barrio")
        print("   • 🚶 Control automático de visitas")
        print("   • 📊 Análisis estadístico de accesos")
        print("   • 💾 Base de datos integrada")
        print()
        print("🔧 Desarrollado con Python + OpenCV + face_recognition")
        print("📅 " + datetime.now().strftime("Fecha: %d/%m/%Y - Hora: %H:%M:%S"))
        print("="*80)
    
    def mostrar_menu_principal(self):
        """
        Muestra el menú principal del sistema.
        """
        print(f"\n🏠 MENÚ PRINCIPAL - BARRIO SEGURO")
        print("="*50)
        print("1. 🎥 Iniciar reconocimiento facial")
        print("2. 👤 Gestión de vecinos")
        print("3. 📊 Análisis y reportes")
        print("4. ⚙️  Configuración del sistema")
        print("5. ℹ️  Información del sistema")
        print("6. 🚪 Salir")
        print("="*50)
    
    def submenu_gestion_vecinos(self):
        """
        Submenú para gestión de vecinos.
        """
        while True:
            print(f"\n👤 GESTIÓN DE VECINOS")
            print("-"*40)
            print("1. 📸 Registrar vecino (cámara)")
            print("2. 📁 Registrar vecino (archivo)")
            print("3. 👥 Listar vecinos registrados")
            print("4. 🗑️  Eliminar vecino")
            print("5. 🔄 Menú completo de registro")
            print("6. ⬅️  Volver al menú principal")
            
            opcion = input("\n🎯 Seleccione una opción (1-6): ").strip()
            
            try:
                registro = RegistroVecino(self.db)
                
                if opcion == '1':
                    nombre = input("👤 Nombre del vecino: ").strip()
                    if nombre:
                        registro.registrar_desde_camara(nombre)
                    else:
                        print("❌ Debe ingresar un nombre válido.")
                
                elif opcion == '2':
                    nombre = input("👤 Nombre del vecino: ").strip()
                    if not nombre:
                        print("❌ Debe ingresar un nombre válido.")
                        continue
                    
                    ruta = input("📁 Ruta de la imagen: ").strip()
                    if not ruta:
                        print("❌ Debe ingresar una ruta válida.")
                        continue
                    
                    if registro.mostrar_preview_imagen(ruta):
                        registro.registrar_desde_archivo(nombre, ruta)
                    else:
                        print("❌ Registro cancelado.")
                
                elif opcion == '3':
                    registro.listar_vecinos_registrados()
                
                elif opcion == '4':
                    nombre = input("👤 Nombre del vecino a eliminar: ").strip()
                    if nombre:
                        registro.eliminar_vecino(nombre)
                    else:
                        print("❌ Debe ingresar un nombre válido.")
                
                elif opcion == '5':
                    print("🔄 Iniciando menú completo de registro...")
                    menu_registro_interactivo()
                
                elif opcion == '6':
                    break
                
                else:
                    print("❌ Opción inválida. Intente nuevamente.")
                    
            except Exception as e:
                logging.error(f"Error en gestión de vecinos: {e}")
                print(f"❌ Error: {e}")
    
    def submenu_analisis(self):
        """
        Submenú para análisis y reportes.
        """
        while True:
            print(f"\n📊 ANÁLISIS Y REPORTES")
            print("-"*40)
            print("1. 📋 Reporte rápido")
            print("2. ⏰ Análisis de horas pico")
            print("3. 📅 Análisis por días")
            print("4. 👥 Vecinos más activos")
            print("5. 💾 Generar reporte completo")
            print("6. 🔧 Menú completo de análisis")
            print("7. ⬅️  Volver al menú principal")
            
            opcion = input("\n🎯 Seleccione una opción (1-7): ").strip()
            
            try:
                analisis = AnalisisRegistros(self.db)
                
                if opcion == '1':
                    analisis.mostrar_reporte_consola()
                
                elif opcion == '2':
                    resultado = analisis.analizar_horas_pico()
                    if 'error' not in resultado:
                        hora_pico = resultado.get('hora_pico', {})
                        hora_valle = resultado.get('hora_valle', {})
                        print(f"\n⏰ ANÁLISIS DE HORAS")
                        print("-"*30)
                        print(f"🔥 Hora pico: {hora_pico.get('hora', 'N/A')} - "
                              f"{hora_pico.get('total_accesos', 0)} accesos")
                        print(f"💤 Hora valle: {hora_valle.get('hora', 'N/A')} - "
                              f"{hora_valle.get('total_accesos', 0)} accesos")
                    else:
                        print(f"❌ {resultado['error']}")
                
                elif opcion == '3':
                    dias = input("📅 Días a analizar (default 7): ").strip()
                    try:
                        dias = int(dias) if dias else 7
                    except ValueError:
                        dias = 7
                    
                    resultado = analisis.analizar_visitas_por_dia(dias)
                    if 'error' not in resultado:
                        resumen = resultado.get('resumen', {})
                        print(f"\n📅 ANÁLISIS DE ÚLTIMOS {dias} DÍAS")
                        print("-"*40)
                        print(f"📊 Total visitas: {resumen.get('total_visitas', 0)}")
                        print(f"📈 Promedio por día: {resumen.get('promedio_visitas_dia', 0)}")
                        print(f"📆 Días con visitas: {resumen.get('dias_con_visitas', 0)}")
                    else:
                        print(f"❌ {resultado['error']}")
                
                elif opcion == '4':
                    resultado = analisis.analizar_vecinos_mas_activos(5)
                    if 'error' not in resultado:
                        print(f"\n👥 TOP 5 VECINOS MÁS ACTIVOS")
                        print("-"*40)
                        for i, vecino in enumerate(resultado.get('vecinos_mas_activos', [])[:5], 1):
                            print(f"{i}. {vecino['nombre']}: {vecino['total_accesos']} accesos")
                    else:
                        print(f"❌ {resultado['error']}")
                
                elif opcion == '5':
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    archivo = f"registros/reporte_completo_{timestamp}.json"
                    resultado = analisis.generar_reporte_completo(archivo)
                    if 'error' not in resultado:
                        print(f"✅ Reporte guardado en: {archivo}")
                    else:
                        print(f"❌ {resultado['error']}")
                
                elif opcion == '6':
                    print("🔧 Iniciando menú completo de análisis...")
                    menu_analisis()
                
                elif opcion == '7':
                    break
                
                else:
                    print("❌ Opción inválida. Intente nuevamente.")
                    
            except Exception as e:
                logging.error(f"Error en análisis: {e}")
                print(f"❌ Error: {e}")
    
    def submenu_configuracion(self):
        """
        Submenú para configuración del sistema.
        """
        while True:
            print(f"\n⚙️ CONFIGURACIÓN DEL SISTEMA")
            print("-"*40)
            print("1. 📹 Configurar cámara")
            print("2. 🎯 Ajustar tolerancia de reconocimiento")
            print("3. ⏱️  Configurar tiempo de visitas")
            print("4. 🔄 Recargar configuración")
            print("5. 💾 Guardar configuración actual")
            print("6. 🔍 Mostrar configuración actual")
            print("7. ⬅️  Volver al menú principal")
            
            opcion = input("\n🎯 Seleccione una opción (1-7): ").strip()
            
            if opcion == '1':
                print("\n📹 CONFIGURACIÓN DE CÁMARA")
                print("-"*30)
                indice_actual = self.config.get('camara_index', 0)
                print(f"Cámara actual: Índice {indice_actual}")
                
                nuevo_indice = input(f"Nuevo índice (actual: {indice_actual}): ").strip()
                if nuevo_indice.isdigit():
                    nuevo_indice = int(nuevo_indice)
                    if verificar_camara(nuevo_indice):
                        self.config['camara_index'] = nuevo_indice
                        print(f"✅ Cámara cambiada al índice {nuevo_indice}")
                    else:
                        print(f"❌ No se puede acceder a la cámara {nuevo_indice}")
                else:
                    print("❌ Índice inválido.")
            
            elif opcion == '2':
                print("\n🎯 TOLERANCIA DE RECONOCIMIENTO")
                print("-"*30)
                tolerancia_actual = self.config.get('tolerancia_reconocimiento', 0.5)
                print(f"Tolerancia actual: {tolerancia_actual}")
                print("(Menor valor = más estricto, Mayor valor = más permisivo)")
                
                nueva_tolerancia = input(f"Nueva tolerancia (0.3-0.7): ").strip()
                try:
                    nueva_tolerancia = float(nueva_tolerancia)
                    if 0.3 <= nueva_tolerancia <= 0.7:
                        self.config['tolerancia_reconocimiento'] = nueva_tolerancia
                        print(f"✅ Tolerancia cambiada a {nueva_tolerancia}")
                    else:
                        print("❌ La tolerancia debe estar entre 0.3 y 0.7")
                except ValueError:
                    print("❌ Valor inválido.")
            
            elif opcion == '3':
                print("\n⏱️ TIEMPO DE VISITAS")
                print("-"*30)
                tiempo_actual = self.config.get('tiempo_visita_minutos', 30)
                print(f"Tiempo actual: {tiempo_actual} minutos")
                
                nuevo_tiempo = input(f"Nuevo tiempo en minutos (5-120): ").strip()
                try:
                    nuevo_tiempo = int(nuevo_tiempo)
                    if 5 <= nuevo_tiempo <= 120:
                        self.config['tiempo_visita_minutos'] = nuevo_tiempo
                        print(f"✅ Tiempo de visitas cambiado a {nuevo_tiempo} minutos")
                    else:
                        print("❌ El tiempo debe estar entre 5 y 120 minutos")
                except ValueError:
                    print("❌ Valor inválido.")
            
            elif opcion == '4':
                from utils import cargar_configuracion
                self.config = cargar_configuracion()
                print("✅ Configuración recargada desde archivo")
            
            elif opcion == '5':
                from utils import guardar_configuracion
                guardar_configuracion(self.config)
                print("✅ Configuración guardada exitosamente")
            
            elif opcion == '6':
                print("\n🔍 CONFIGURACIÓN ACTUAL")
                print("-"*30)
                for clave, valor in self.config.items():
                    print(f"• {clave}: {valor}")
            
            elif opcion == '7':
                break
            
            else:
                print("❌ Opción inválida. Intente nuevamente.")
    
    def mostrar_info_sistema(self):
        """
        Muestra información del sistema y diagnósticos.
        """
        print("\nℹ️ INFORMACIÓN DEL SISTEMA")
        print("="*40)
        
        # Información básica
        print(f"🏠 Sistema: Barrio Seguro v{self.version}")
        print(f"📅 Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        
        # Información técnica
        info = obtener_info_sistema()
        print(f"\n🔧 INFORMACIÓN TÉCNICA")
        print("-"*30)
        print(f"• OpenCV: {info.get('opencv_version', 'No disponible')}")
        print(f"• Face Recognition: {'Disponible' if info.get('face_recognition_disponible') else 'No disponible'}")
        print(f"• Cámara: {'Disponible' if info.get('camara_disponible') else 'No disponible'}")
        print(f"• Python: {info.get('python_version', 'Desconocido')}")
        
        # Estadísticas de la base de datos
        try:
            stats = self.db.obtener_estadisticas_accesos()
            print(f"\n📊 ESTADÍSTICAS DE BASE DE DATOS")
            print("-"*30)
            print(f"• Vecinos registrados: {len(self.db.obtener_vecinos_activos())}")
            
            # Total de accesos
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM accesos")
                total_accesos = cursor.fetchone()[0]
                print(f"• Total de accesos: {total_accesos}")
                
        except Exception as e:
            print(f"❌ Error al obtener estadísticas: {e}")
        
        print("\n📁 ESTRUCTURA DEL PROYECTO")
        print("-"*30)
        directorios = ['dataset/vecinos', 'dataset/visitas', 'registros']
        for directorio in directorios:
            if os.path.exists(directorio):
                archivos = len([f for f in os.listdir(directorio) if os.path.isfile(os.path.join(directorio, f))])
                print(f"• {directorio}: {archivos} archivos")
            else:
                print(f"• {directorio}: No existe")
    
    def ejecutar(self):
        """
        Ejecuta el sistema principal con el menú interactivo.
        """
        try:
            # Mostrar bienvenida
            self.mostrar_bienvenida()
            
            # Inicializar sistema
            if not self.inicializar_sistema():
                print("❌ No se pudo inicializar el sistema. Abortando.")
                return
            
            print("✅ Sistema inicializado correctamente")
            input("\n🎯 Presione ENTER para continuar...")
            
            # Bucle principal del menú
            while True:
                try:
                    self.mostrar_menu_principal()
                    opcion = input("\n🎯 Seleccione una opción (1-6): ").strip()
                    
                    if opcion == '1':
                        print("\n🎥 Iniciando sistema de reconocimiento facial...")
                        print("⚠️  Presione 'q' en la ventana de video para salir")
                        input("🎯 Presione ENTER para continuar...")
                        
                        try:
                            sistema_reconocimiento = SistemaReconocimiento(self.config)
                            sistema_reconocimiento.iniciar_reconocimiento()
                        except Exception as e:
                            logging.error(f"Error en reconocimiento: {e}")
                            print(f"❌ Error en reconocimiento: {e}")
                    
                    elif opcion == '2':
                        self.submenu_gestion_vecinos()
                    
                    elif opcion == '3':
                        self.submenu_analisis()
                    
                    elif opcion == '4':
                        self.submenu_configuracion()
                    
                    elif opcion == '5':
                        self.mostrar_info_sistema()
                        input("\n🎯 Presione ENTER para continuar...")
                    
                    elif opcion == '6':
                        print("\n👋 ¡Gracias por usar Barrio Seguro!")
                        print("🔒 Sistema finalizado de forma segura.")
                        logging.info("Sistema finalizado por el usuario")
                        break
                    
                    else:
                        print("❌ Opción inválida. Por favor seleccione una opción válida (1-6).")
                        input("🎯 Presione ENTER para continuar...")
                
                except KeyboardInterrupt:
                    print("\n\n🛑 Interrupción detectada.")
                    confirmacion = input("❓ ¿Desea salir del sistema? (s/N): ").strip().lower()
                    if confirmacion == 's':
                        break
                
                except Exception as e:
                    logging.error(f"Error en menú principal: {e}")
                    print(f"❌ Error inesperado: {e}")
                    input("🎯 Presione ENTER para continuar...")
        
        except Exception as e:
            logging.error(f"Error crítico en sistema principal: {e}")
            print(f"❌ Error crítico: {e}")
        
        finally:
            print("\n🔒 Finalizando sistema...")
            logging.info("Sistema Barrio Seguro finalizado")


def main():
    """
    Función principal del programa.
    """
    try:
        # Verificar Python y dependencias
        print("🔧 Verificando dependencias...")
        
        try:
            import cv2
            import face_recognition
            import sqlite3
            import numpy
            print("✅ Todas las dependencias están disponibles")
        except ImportError as e:
            print(f"❌ Dependencia faltante: {e}")
            print("\n📋 Para instalar las dependencias ejecute:")
            print("   pip install opencv-python face_recognition numpy sqlite3")
            return
        
        # Crear e inicializar sistema
        sistema = SistemaBarrioSeguro()
        sistema.ejecutar()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Sistema interrumpido por el usuario.")
    except Exception as e:
        print(f"❌ Error crítico al iniciar: {e}")
        logging.error(f"Error crítico en main: {e}")


if __name__ == "__main__":
    main()