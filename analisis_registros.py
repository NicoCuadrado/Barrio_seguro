"""
Módulo de Análisis de Registros - Sistema Barrio Seguro
=======================================================
Sistema de análisis estadístico de accesos y generación de informes.

Autor: Sistema Barrio Seguro
Fecha: 23/10/2025
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import json
import os

from base_datos import BaseDatos
from utils import configurar_logging, formatear_tiempo_transcurrido


class AnalisisRegistros:
    """
    Clase para análisis estadístico de registros de acceso.
    """
    
    def __init__(self, db: BaseDatos = None):
        """
        Inicializa el sistema de análisis.
        
        Args:
            db (BaseDatos): Instancia de la base de datos
        """
        self.db = db or BaseDatos()
        
    def obtener_estadisticas_generales(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas generales del sistema.
        
        Returns:
            Dict: Estadísticas generales
        """
        try:
            stats = self.db.obtener_estadisticas_accesos()
            
            # Estadísticas adicionales
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de vecinos registrados
                cursor.execute("SELECT COUNT(*) FROM vecinos WHERE activo = 1")
                total_vecinos = cursor.fetchone()[0]
                
                # Total de accesos
                cursor.execute("SELECT COUNT(*) FROM accesos")
                total_accesos = cursor.fetchone()[0]
                
                # Accesos de hoy
                cursor.execute("""
                    SELECT COUNT(*) FROM accesos 
                    WHERE DATE(fecha_hora) = DATE('now')
                """)
                accesos_hoy = cursor.fetchone()[0]
                
                # Accesos de esta semana
                cursor.execute("""
                    SELECT COUNT(*) FROM accesos 
                    WHERE fecha_hora >= DATE('now', '-7 days')
                """)
                accesos_semana = cursor.fetchone()[0]
                
                # Primer y último acceso
                cursor.execute("""
                    SELECT MIN(fecha_hora), MAX(fecha_hora) FROM accesos
                """)
                primer_acceso, ultimo_acceso = cursor.fetchone()
            
            return {
                'total_vecinos': total_vecinos,
                'total_accesos': total_accesos,
                'accesos_hoy': accesos_hoy,
                'accesos_semana': accesos_semana,
                'primer_acceso': primer_acceso,
                'ultimo_acceso': ultimo_acceso,
                'estadisticas_db': stats
            }
            
        except Exception as e:
            logging.error(f"Error al obtener estadísticas generales: {e}")
            return {}
    
    def analizar_horas_pico(self) -> Dict[str, Any]:
        """
        Analiza las horas con más y menos ingresos.
        
        Returns:
            Dict: Análisis de horas pico
        """
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Accesos por hora
                cursor.execute("""
                    SELECT 
                        strftime('%H', fecha_hora) as hora,
                        COUNT(*) as total_accesos,
                        COUNT(CASE WHEN tipo_persona = 'vecino' THEN 1 END) as accesos_vecinos,
                        COUNT(CASE WHEN tipo_persona = 'visita' THEN 1 END) as accesos_visitas
                    FROM accesos 
                    GROUP BY hora 
                    ORDER BY total_accesos DESC
                """)
                
                datos_horas = cursor.fetchall()
                
                if not datos_horas:
                    return {'error': 'No hay datos de accesos disponibles'}
                
                # Convertir a diccionario más manejable
                accesos_por_hora = {}
                for hora, total, vecinos, visitas in datos_horas:
                    accesos_por_hora[int(hora)] = {
                        'total': total,
                        'vecinos': vecinos,
                        'visitas': visitas
                    }
                
                # Encontrar horas pico y valle
                hora_pico = datos_horas[0]  # Primera = mayor tráfico
                hora_valle = datos_horas[-1]  # Última = menor tráfico
                
                # Calcular promedios por franjas horarias
                franja_mañana = sum(accesos_por_hora.get(h, {}).get('total', 0) for h in range(6, 12))
                franja_tarde = sum(accesos_por_hora.get(h, {}).get('total', 0) for h in range(12, 18))
                franja_noche = sum(accesos_por_hora.get(h, {}).get('total', 0) for h in range(18, 24))
                franja_madrugada = sum(accesos_por_hora.get(h, {}).get('total', 0) for h in range(0, 6))
                
                return {
                    'accesos_por_hora': accesos_por_hora,
                    'hora_pico': {
                        'hora': f"{hora_pico[0]}:00",
                        'total_accesos': hora_pico[1],
                        'vecinos': hora_pico[2],
                        'visitas': hora_pico[3]
                    },
                    'hora_valle': {
                        'hora': f"{hora_valle[0]}:00",
                        'total_accesos': hora_valle[1],
                        'vecinos': hora_valle[2],
                        'visitas': hora_valle[3]
                    },
                    'franjas_horarias': {
                        'mañana (6-12h)': franja_mañana,
                        'tarde (12-18h)': franja_tarde,
                        'noche (18-24h)': franja_noche,
                        'madrugada (0-6h)': franja_madrugada
                    }
                }
                
        except Exception as e:
            logging.error(f"Error al analizar horas pico: {e}")
            return {'error': str(e)}
    
    def analizar_visitas_por_dia(self, dias: int = 30) -> Dict[str, Any]:
        """
        Analiza la cantidad de visitas por día.
        
        Args:
            dias (int): Número de días a analizar
            
        Returns:
            Dict: Análisis de visitas por día
        """
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT 
                        DATE(fecha_hora) as fecha,
                        COUNT(*) as total_accesos,
                        COUNT(CASE WHEN tipo_persona = 'vecino' THEN 1 END) as accesos_vecinos,
                        COUNT(CASE WHEN tipo_persona = 'visita' THEN 1 END) as accesos_visitas,
                        COUNT(DISTINCT nombre) as personas_unicas
                    FROM accesos 
                    WHERE fecha_hora >= DATE('now', '-{} days')
                    GROUP BY fecha 
                    ORDER BY fecha DESC
                """.format(dias))
                
                datos_dias = cursor.fetchall()
                
                if not datos_dias:
                    return {'error': f'No hay datos de los últimos {dias} días'}
                
                # Procesar datos
                datos_procesados = []
                total_visitas = 0
                total_accesos = 0
                dias_con_visitas = 0
                
                for fecha, total, vecinos, visitas, personas in datos_dias:
                    datos_procesados.append({
                        'fecha': fecha,
                        'total_accesos': total,
                        'vecinos': vecinos,
                        'visitas': visitas,
                        'personas_unicas': personas
                    })
                    
                    total_visitas += visitas
                    total_accesos += total
                    if visitas > 0:
                        dias_con_visitas += 1
                
                # Calcular promedios
                dias_analizados = len(datos_dias)
                promedio_visitas_dia = total_visitas / dias_analizados if dias_analizados > 0 else 0
                promedio_accesos_dia = total_accesos / dias_analizados if dias_analizados > 0 else 0
                
                # Día con más y menos visitas
                dia_mas_visitas = max(datos_procesados, key=lambda x: x['visitas']) if datos_procesados else None
                dia_menos_visitas = min(datos_procesados, key=lambda x: x['visitas']) if datos_procesados else None
                
                return {
                    'datos_diarios': datos_procesados,
                    'resumen': {
                        'dias_analizados': dias_analizados,
                        'total_visitas': total_visitas,
                        'total_accesos': total_accesos,
                        'dias_con_visitas': dias_con_visitas,
                        'promedio_visitas_dia': round(promedio_visitas_dia, 2),
                        'promedio_accesos_dia': round(promedio_accesos_dia, 2)
                    },
                    'extremos': {
                        'dia_mas_visitas': dia_mas_visitas,
                        'dia_menos_visitas': dia_menos_visitas
                    }
                }
                
        except Exception as e:
            logging.error(f"Error al analizar visitas por día: {e}")
            return {'error': str(e)}
    
    def analizar_vecinos_mas_activos(self, limite: int = 10) -> Dict[str, Any]:
        """
        Analiza los vecinos con mayor frecuencia de entrada/salida.
        
        Args:
            limite (int): Número máximo de vecinos a mostrar
            
        Returns:
            Dict: Análisis de vecinos más activos
        """
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Vecinos más activos por total de accesos
                cursor.execute("""
                    SELECT 
                        nombre,
                        COUNT(*) as total_accesos,
                        COUNT(CASE WHEN tipo_evento = 'entrada' THEN 1 END) as entradas,
                        COUNT(CASE WHEN tipo_evento = 'salida' THEN 1 END) as salidas,
                        MIN(fecha_hora) as primer_acceso,
                        MAX(fecha_hora) as ultimo_acceso
                    FROM accesos 
                    WHERE tipo_persona = 'vecino'
                    GROUP BY nombre 
                    ORDER BY total_accesos DESC
                    LIMIT ?
                """, (limite,))
                
                vecinos_activos = cursor.fetchall()
                
                # Vecinos por frecuencia (accesos por día)
                cursor.execute("""
                    SELECT 
                        nombre,
                        COUNT(*) as total_accesos,
                        COUNT(DISTINCT DATE(fecha_hora)) as dias_activos,
                        ROUND(CAST(COUNT(*) AS FLOAT) / COUNT(DISTINCT DATE(fecha_hora)), 2) as accesos_por_dia
                    FROM accesos 
                    WHERE tipo_persona = 'vecino'
                    GROUP BY nombre 
                    HAVING dias_activos > 0
                    ORDER BY accesos_por_dia DESC
                    LIMIT ?
                """, (limite,))
                
                vecinos_por_frecuencia = cursor.fetchall()
                
                # Procesar datos
                datos_actividad = []
                for nombre, total, entradas, salidas, primer, ultimo in vecinos_activos:
                    datos_actividad.append({
                        'nombre': nombre,
                        'total_accesos': total,
                        'entradas': entradas,
                        'salidas': salidas,
                        'primer_acceso': primer,
                        'ultimo_acceso': ultimo,
                        'balance': entradas - salidas  # Positivo = más entradas que salidas
                    })
                
                datos_frecuencia = []
                for nombre, total, dias, frecuencia in vecinos_por_frecuencia:
                    datos_frecuencia.append({
                        'nombre': nombre,
                        'total_accesos': total,
                        'dias_activos': dias,
                        'accesos_por_dia': frecuencia
                    })
                
                return {
                    'vecinos_mas_activos': datos_actividad,
                    'vecinos_por_frecuencia': datos_frecuencia,
                    'total_vecinos_con_accesos': len(vecinos_activos)
                }
                
        except Exception as e:
            logging.error(f"Error al analizar vecinos activos: {e}")
            return {'error': str(e)}
    
    def generar_reporte_completo(self, archivo_salida: str = None) -> Dict[str, Any]:
        """
        Genera un reporte completo del sistema.
        
        Args:
            archivo_salida (str): Ruta del archivo de salida (opcional)
            
        Returns:
            Dict: Reporte completo
        """
        try:
            print("📊 Generando reporte completo...")
            
            # Obtener todos los análisis
            stats_generales = self.obtener_estadisticas_generales()
            analisis_horas = self.analizar_horas_pico()
            analisis_visitas = self.analizar_visitas_por_dia()
            analisis_vecinos = self.analizar_vecinos_mas_activos()
            
            reporte = {
                'metadata': {
                    'fecha_generacion': datetime.now().isoformat(),
                    'sistema': 'Barrio Seguro - Control de Acceso',
                    'version': '1.0'
                },
                'estadisticas_generales': stats_generales,
                'analisis_horas_pico': analisis_horas,
                'analisis_visitas_diarias': analisis_visitas,
                'analisis_vecinos_activos': analisis_vecinos
            }
            
            # Guardar en archivo si se especifica
            if archivo_salida:
                try:
                    os.makedirs(os.path.dirname(archivo_salida), exist_ok=True)
                    with open(archivo_salida, 'w', encoding='utf-8') as f:
                        json.dump(reporte, f, indent=4, ensure_ascii=False, default=str)
                    print(f"✅ Reporte guardado en: {archivo_salida}")
                except Exception as e:
                    print(f"⚠️  Error al guardar archivo: {e}")
            
            return reporte
            
        except Exception as e:
            logging.error(f"Error al generar reporte: {e}")
            return {'error': str(e)}
    
    def mostrar_reporte_consola(self):
        """
        Muestra un reporte formateado en la consola.
        """
        try:
            print("\n" + "="*80)
            print("📊 REPORTE DE ANÁLISIS - SISTEMA BARRIO SEGURO")
            print("="*80)
            
            # Estadísticas generales
            stats = self.obtener_estadisticas_generales()
            print(f"\n📋 ESTADÍSTICAS GENERALES")
            print("-" * 40)
            print(f"👥 Vecinos registrados: {stats.get('total_vecinos', 0)}")
            print(f"🚪 Total de accesos: {stats.get('total_accesos', 0)}")
            print(f"📅 Accesos hoy: {stats.get('accesos_hoy', 0)}")
            print(f"📊 Accesos esta semana: {stats.get('accesos_semana', 0)}")
            
            if stats.get('primer_acceso'):
                print(f"🔍 Primer acceso: {stats['primer_acceso']}")
            if stats.get('ultimo_acceso'):
                print(f"⏰ Último acceso: {stats['ultimo_acceso']}")
            
            # Análisis de horas pico
            horas = self.analizar_horas_pico()
            if 'error' not in horas:
                print(f"\n⏰ ANÁLISIS DE HORAS PICO")
                print("-" * 40)
                hora_pico = horas.get('hora_pico', {})
                hora_valle = horas.get('hora_valle', {})
                
                print(f"🔥 Hora pico: {hora_pico.get('hora', 'N/A')} "
                      f"({hora_pico.get('total_accesos', 0)} accesos)")
                print(f"💤 Hora valle: {hora_valle.get('hora', 'N/A')} "
                      f"({hora_valle.get('total_accesos', 0)} accesos)")
                
                franjas = horas.get('franjas_horarias', {})
                print(f"\n📊 Accesos por franja horaria:")
                for franja, total in franjas.items():
                    print(f"   • {franja}: {total} accesos")
            
            # Análisis de visitas
            visitas = self.analizar_visitas_por_dia(7)  # Últimos 7 días
            if 'error' not in visitas:
                print(f"\n🚶 ANÁLISIS DE VISITAS (últimos 7 días)")
                print("-" * 40)
                resumen = visitas.get('resumen', {})
                print(f"📊 Total visitas: {resumen.get('total_visitas', 0)}")
                print(f"📅 Días con visitas: {resumen.get('dias_con_visitas', 0)}")
                print(f"📈 Promedio por día: {resumen.get('promedio_visitas_dia', 0)}")
                
                extremos = visitas.get('extremos', {})
                dia_mas = extremos.get('dia_mas_visitas', {})
                if dia_mas:
                    print(f"🔝 Día con más visitas: {dia_mas.get('fecha')} "
                          f"({dia_mas.get('visitas')} visitas)")
            
            # Vecinos más activos
            vecinos = self.analizar_vecinos_mas_activos(5)  # Top 5
            if 'error' not in vecinos:
                print(f"\n👥 VECINOS MÁS ACTIVOS (Top 5)")
                print("-" * 40)
                activos = vecinos.get('vecinos_mas_activos', [])
                
                for i, vecino in enumerate(activos[:5], 1):
                    print(f"{i}. {vecino['nombre']}: {vecino['total_accesos']} accesos "
                          f"(E:{vecino['entradas']}, S:{vecino['salidas']})")
                
                print(f"\n🔍 Total vecinos con accesos: {vecinos.get('total_vecinos_con_accesos', 0)}")
            
            print("\n" + "="*80)
            print(f"📅 Reporte generado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            print("="*80)
            
        except Exception as e:
            logging.error(f"Error al mostrar reporte: {e}")
            print(f"❌ Error al generar reporte: {e}")
    
    def limpiar_datos_antiguos(self, dias_limite: int = 90) -> int:
        """
        Limpia registros de acceso más antiguos que el límite especificado.
        
        Args:
            dias_limite (int): Días después de los cuales eliminar registros
            
        Returns:
            int: Número de registros eliminados
        """
        try:
            with sqlite3.connect(self.db.db_path) as conn:
                cursor = conn.cursor()
                
                # Contar registros que se van a eliminar
                cursor.execute("""
                    SELECT COUNT(*) FROM accesos 
                    WHERE fecha_hora < DATE('now', '-{} days')
                """.format(dias_limite))
                
                registros_a_eliminar = cursor.fetchone()[0]
                
                if registros_a_eliminar == 0:
                    print(f"ℹ️  No hay registros anteriores a {dias_limite} días para eliminar.")
                    return 0
                
                print(f"⚠️  Se eliminarán {registros_a_eliminar} registros anteriores a {dias_limite} días.")
                confirmacion = input("❓ ¿Continuar? (s/N): ").strip().lower()
                
                if confirmacion == 's':
                    # Eliminar registros antiguos
                    cursor.execute("""
                        DELETE FROM accesos 
                        WHERE fecha_hora < DATE('now', '-{} days')
                    """.format(dias_limite))
                    
                    eliminados = cursor.rowcount
                    conn.commit()
                    
                    print(f"✅ {eliminados} registros eliminados exitosamente.")
                    logging.info(f"Limpieza de datos: {eliminados} registros eliminados")
                    return eliminados
                else:
                    print("❌ Limpieza cancelada.")
                    return 0
                    
        except Exception as e:
            logging.error(f"Error en limpieza de datos: {e}")
            print(f"❌ Error en limpieza: {e}")
            return 0


def menu_analisis():
    """
    Menú interactivo para análisis de registros.
    """
    try:
        configurar_logging()
        
        print("\n📊 SISTEMA DE ANÁLISIS DE REGISTROS")
        print("="*50)
        
        analisis = AnalisisRegistros()
        
        while True:
            print(f"\n📋 MENÚ DE ANÁLISIS")
            print("-" * 30)
            print("1. 📊 Mostrar reporte completo")
            print("2. ⏰ Análisis de horas pico")
            print("3. 🚶 Análisis de visitas por día")
            print("4. 👥 Vecinos más activos")
            print("5. 💾 Generar reporte JSON")
            print("6. 🧹 Limpiar datos antiguos")
            print("7. 🚪 Salir")
            
            opcion = input("\n🎯 Seleccione una opción (1-7): ").strip()
            
            if opcion == '1':
                analisis.mostrar_reporte_consola()
            
            elif opcion == '2':
                horas = analisis.analizar_horas_pico()
                print("\n⏰ ANÁLISIS DETALLADO DE HORAS")
                print("="*50)
                
                if 'error' in horas:
                    print(f"❌ Error: {horas['error']}")
                else:
                    # Mostrar datos por hora
                    por_hora = horas.get('accesos_por_hora', {})
                    print("\n📊 Accesos por hora:")
                    for hora in range(24):
                        data = por_hora.get(hora, {'total': 0, 'vecinos': 0, 'visitas': 0})
                        if data['total'] > 0:
                            print(f"  {hora:02d}:00 - {data['total']:3d} accesos "
                                  f"(V:{data['vecinos']:2d}, VS:{data['visitas']:2d})")
            
            elif opcion == '3':
                dias = input("📅 Días a analizar (por defecto 30): ").strip()
                try:
                    dias = int(dias) if dias else 30
                except ValueError:
                    dias = 30
                
                visitas = analisis.analizar_visitas_por_dia(dias)
                print(f"\n🚶 ANÁLISIS DE VISITAS ({dias} días)")
                print("="*50)
                
                if 'error' in visitas:
                    print(f"❌ Error: {visitas['error']}")
                else:
                    # Mostrar datos diarios recientes
                    datos = visitas.get('datos_diarios', [])[:10]  # Solo últimos 10 días
                    print("\n📅 Últimos días:")
                    for dia in datos:
                        print(f"  {dia['fecha']}: {dia['total_accesos']} accesos "
                              f"({dia['vecinos']} vecinos, {dia['visitas']} visitas)")
            
            elif opcion == '4':
                limite = input("👥 Número de vecinos a mostrar (por defecto 10): ").strip()
                try:
                    limite = int(limite) if limite else 10
                except ValueError:
                    limite = 10
                
                vecinos = analisis.analizar_vecinos_mas_activos(limite)
                print(f"\n👥 VECINOS MÁS ACTIVOS (Top {limite})")
                print("="*50)
                
                if 'error' in vecinos:
                    print(f"❌ Error: {vecinos['error']}")
                else:
                    activos = vecinos.get('vecinos_mas_activos', [])
                    for i, vecino in enumerate(activos, 1):
                        print(f"{i:2d}. {vecino['nombre']}")
                        print(f"     📊 Total: {vecino['total_accesos']} accesos")
                        print(f"     ↗️  Entradas: {vecino['entradas']}")
                        print(f"     ↙️  Salidas: {vecino['salidas']}")
                        print(f"     ⚖️  Balance: {vecino['balance']}")
                        print(f"     📅 Último: {vecino['ultimo_acceso']}")
                        print()
            
            elif opcion == '5':
                nombre_archivo = input("💾 Nombre del archivo (default: reporte.json): ").strip()
                if not nombre_archivo:
                    nombre_archivo = f"registros/reporte_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                
                reporte = analisis.generar_reporte_completo(nombre_archivo)
                if 'error' not in reporte:
                    print("✅ Reporte JSON generado exitosamente")
            
            elif opcion == '6':
                dias = input("🧹 Eliminar registros anteriores a (días, default 90): ").strip()
                try:
                    dias = int(dias) if dias else 90
                except ValueError:
                    dias = 90
                
                eliminados = analisis.limpiar_datos_antiguos(dias)
                
            elif opcion == '7':
                print("👋 ¡Hasta luego!")
                break
            
            else:
                print("❌ Opción inválida. Intente nuevamente.")
                
    except KeyboardInterrupt:
        print("\n\n👋 Sistema interrumpido por el usuario.")
    except Exception as e:
        logging.error(f"Error en menú de análisis: {e}")
        print(f"❌ Error en el sistema: {e}")


if __name__ == "__main__":
    menu_analisis()