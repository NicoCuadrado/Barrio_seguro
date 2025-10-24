"""
Sistema de Base de Datos para Barrio Seguro
===========================================
Módulo para manejar la base de datos SQLite del sistema de reconocimiento facial.
Gestiona vecinos, accesos y visitas del barrio privado.

Autor: Sistema Barrio Seguro
Fecha: 23/10/2025
"""

import sqlite3
import os
import pickle
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
import logging


class BaseDatos:
    """
    Clase para manejar todas las operaciones de base de datos.
    """
    
    def __init__(self, db_path: str = "registros/accesos.db"):
        """
        Inicializa la conexión a la base de datos.
        
        Args:
            db_path (str): Ruta al archivo de base de datos
        """
        self.db_path = db_path
        self.crear_tablas()
        
    def crear_tablas(self):
        """
        Crea las tablas necesarias si no existen.
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Tabla de vecinos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS vecinos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL UNIQUE,
                        ruta_imagen TEXT NOT NULL,
                        encoding BLOB NOT NULL,
                        fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        activo BOOLEAN DEFAULT 1
                    )
                """)
                
                # Tabla de accesos
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS accesos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        tipo_persona TEXT NOT NULL,  -- 'vecino' o 'visita'
                        tipo_evento TEXT NOT NULL,   -- 'entrada', 'salida'
                        fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        ruta_imagen TEXT
                    )
                """)
                
                # Tabla de visitas temporales
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS visitas_temporales (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre_archivo TEXT NOT NULL UNIQUE,
                        encoding BLOB NOT NULL,
                        fecha_entrada TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        activa BOOLEAN DEFAULT 1
                    )
                """)
                
                conn.commit()
                logging.info("Tablas de base de datos creadas/verificadas exitosamente")
                
        except sqlite3.Error as e:
            logging.error(f"Error al crear tablas: {e}")
            raise
    
    def registrar_vecino(self, nombre: str, ruta_imagen: str, encoding) -> bool:
        """
        Registra un nuevo vecino en la base de datos.
        
        Args:
            nombre (str): Nombre del vecino
            ruta_imagen (str): Ruta a la imagen del vecino
            encoding: Codificación facial del vecino
            
        Returns:
            bool: True si se registró correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Serializar el encoding
                encoding_bytes = pickle.dumps(encoding)
                
                cursor.execute("""
                    INSERT INTO vecinos (nombre, ruta_imagen, encoding)
                    VALUES (?, ?, ?)
                """, (nombre, ruta_imagen, encoding_bytes))
                
                conn.commit()
                logging.info(f"Vecino {nombre} registrado exitosamente")
                return True
                
        except sqlite3.IntegrityError:
            logging.warning(f"El vecino {nombre} ya existe en la base de datos")
            return False
        except sqlite3.Error as e:
            logging.error(f"Error al registrar vecino: {e}")
            return False
    
    def obtener_vecinos_activos(self) -> List[Tuple]:
        """
        Obtiene todos los vecinos activos.
        
        Returns:
            List[Tuple]: Lista de tuplas (id, nombre, encoding)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, encoding FROM vecinos 
                    WHERE activo = 1
                """)
                
                vecinos = []
                for row in cursor.fetchall():
                    id_vecino, nombre, encoding_bytes = row
                    encoding = pickle.loads(encoding_bytes)
                    vecinos.append((id_vecino, nombre, encoding))
                
                return vecinos
                
        except sqlite3.Error as e:
            logging.error(f"Error al obtener vecinos: {e}")
            return []
    
    def registrar_acceso(self, nombre: str, tipo_persona: str, tipo_evento: str, 
                        ruta_imagen: str = None) -> bool:
        """
        Registra un acceso en la base de datos.
        
        Args:
            nombre (str): Nombre de la persona
            tipo_persona (str): 'vecino' o 'visita'
            tipo_evento (str): 'entrada' o 'salida'
            ruta_imagen (str): Ruta a la imagen (opcional)
            
        Returns:
            bool: True si se registró correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO accesos (nombre, tipo_persona, tipo_evento, ruta_imagen)
                    VALUES (?, ?, ?, ?)
                """, (nombre, tipo_persona, tipo_evento, ruta_imagen))
                
                conn.commit()
                logging.info(f"Acceso registrado: {nombre} - {tipo_evento}")
                return True
                
        except sqlite3.Error as e:
            logging.error(f"Error al registrar acceso: {e}")
            return False
    
    def registrar_visita_temporal(self, nombre_archivo: str, encoding) -> bool:
        """
        Registra una visita temporal.
        
        Args:
            nombre_archivo (str): Nombre del archivo de imagen
            encoding: Codificación facial
            
        Returns:
            bool: True si se registró correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                encoding_bytes = pickle.dumps(encoding)
                
                cursor.execute("""
                    INSERT INTO visitas_temporales (nombre_archivo, encoding)
                    VALUES (?, ?)
                """, (nombre_archivo, encoding_bytes))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            logging.error(f"Error al registrar visita temporal: {e}")
            return False
    
    def obtener_visitas_temporales_activas(self) -> List[Tuple]:
        """
        Obtiene todas las visitas temporales activas.
        
        Returns:
            List[Tuple]: Lista de tuplas (id, nombre_archivo, encoding, fecha_entrada)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre_archivo, encoding, fecha_entrada 
                    FROM visitas_temporales 
                    WHERE activa = 1
                """)
                
                visitas = []
                for row in cursor.fetchall():
                    id_visita, nombre_archivo, encoding_bytes, fecha_entrada = row
                    encoding = pickle.loads(encoding_bytes)
                    visitas.append((id_visita, nombre_archivo, encoding, fecha_entrada))
                
                return visitas
                
        except sqlite3.Error as e:
            logging.error(f"Error al obtener visitas temporales: {e}")
            return []
    
    def desactivar_visita_temporal(self, id_visita: int) -> bool:
        """
        Desactiva una visita temporal.
        
        Args:
            id_visita (int): ID de la visita
            
        Returns:
            bool: True si se desactivó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE visitas_temporales 
                    SET activa = 0 
                    WHERE id = ?
                """, (id_visita,))
                
                conn.commit()
                return True
                
        except sqlite3.Error as e:
            logging.error(f"Error al desactivar visita temporal: {e}")
            return False
    
    def obtener_estadisticas_accesos(self) -> Dict[str, Any]:
        """
        Obtiene estadísticas de accesos.
        
        Returns:
            Dict: Diccionario con estadísticas
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total de accesos por tipo
                cursor.execute("""
                    SELECT tipo_persona, tipo_evento, COUNT(*) 
                    FROM accesos 
                    GROUP BY tipo_persona, tipo_evento
                """)
                accesos_por_tipo = cursor.fetchall()
                
                # Accesos por hora
                cursor.execute("""
                    SELECT strftime('%H', fecha_hora) as hora, COUNT(*) 
                    FROM accesos 
                    GROUP BY hora 
                    ORDER BY COUNT(*) DESC
                """)
                accesos_por_hora = cursor.fetchall()
                
                # Vecinos más activos
                cursor.execute("""
                    SELECT nombre, COUNT(*) as total_accesos
                    FROM accesos 
                    WHERE tipo_persona = 'vecino'
                    GROUP BY nombre 
                    ORDER BY total_accesos DESC
                    LIMIT 10
                """)
                vecinos_activos = cursor.fetchall()
                
                # Accesos por día
                cursor.execute("""
                    SELECT DATE(fecha_hora) as fecha, 
                           COUNT(*) as total_accesos,
                           SUM(CASE WHEN tipo_persona = 'visita' THEN 1 ELSE 0 END) as visitas
                    FROM accesos 
                    GROUP BY fecha 
                    ORDER BY fecha DESC
                    LIMIT 30
                """)
                accesos_por_dia = cursor.fetchall()
                
                return {
                    'accesos_por_tipo': accesos_por_tipo,
                    'accesos_por_hora': accesos_por_hora,
                    'vecinos_activos': vecinos_activos,
                    'accesos_por_dia': accesos_por_dia
                }
                
        except sqlite3.Error as e:
            logging.error(f"Error al obtener estadísticas: {e}")
            return {}
    
    def buscar_vecino_por_nombre(self, nombre: str) -> Optional[Tuple]:
        """
        Busca un vecino por nombre.
        
        Args:
            nombre (str): Nombre del vecino
            
        Returns:
            Optional[Tuple]: Información del vecino o None
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT id, nombre, ruta_imagen, fecha_registro, activo
                    FROM vecinos 
                    WHERE nombre = ? AND activo = 1
                """, (nombre,))
                
                return cursor.fetchone()
                
        except sqlite3.Error as e:
            logging.error(f"Error al buscar vecino: {e}")
            return None
    
    def eliminar_vecino(self, nombre: str) -> bool:
        """
        Desactiva un vecino (eliminación lógica).
        
        Args:
            nombre (str): Nombre del vecino
            
        Returns:
            bool: True si se desactivó correctamente
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    UPDATE vecinos 
                    SET activo = 0 
                    WHERE nombre = ?
                """, (nombre,))
                
                conn.commit()
                return cursor.rowcount > 0
                
        except sqlite3.Error as e:
            logging.error(f"Error al eliminar vecino: {e}")
            return False