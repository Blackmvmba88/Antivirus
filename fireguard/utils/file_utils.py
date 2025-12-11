"""
File Utils - Utilidades de Archivos

Este módulo proporciona funciones auxiliares para manejo de archivos,
incluyendo escaneo, hash, cuarentena y otras operaciones relacionadas
con archivos del sistema.
"""

import hashlib
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any


class FileUtils:
    """
    Utilidades para manejo de archivos.
    
    Proporciona funciones auxiliares para operaciones con archivos
    en el contexto del antivirus.
    """
    
    def __init__(self):
        """Inicializa las utilidades de archivos."""
        self.logger = logging.getLogger(__name__)
    
    @staticmethod
    def calculate_hash(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Calcula el hash de un archivo.
        
        Args:
            file_path: Ruta al archivo
            algorithm: Algoritmo de hash (md5, sha1, sha256)
            
        Returns:
            Hash del archivo o None si hay error
        """
        try:
            hash_func = getattr(hashlib, algorithm)()
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
        
        except Exception as e:
            logging.error(f"Error calculando hash de {file_path}: {e}")
            return None
    
    @staticmethod
    def is_executable(file_path: str) -> bool:
        """
        Verifica si un archivo es ejecutable.
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            True si el archivo es ejecutable
        """
        path = Path(file_path)
        if not path.exists():
            return False
        
        # Extensiones comunes de ejecutables
        executable_extensions = [
            '.exe', '.dll', '.com', '.bat', '.cmd', '.msi',
            '.sh', '.bin', '.run', '.app', '.deb', '.rpm'
        ]
        
        return path.suffix.lower() in executable_extensions
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict[str, Any]:
        """
        Obtiene información detallada de un archivo.
        
        Args:
            file_path: Ruta al archivo
            
        Returns:
            Diccionario con información del archivo
        """
        path = Path(file_path)
        
        if not path.exists():
            return {"error": "File not found"}
        
        stat = path.stat()
        
        return {
            "name": path.name,
            "path": str(path.absolute()),
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "is_file": path.is_file(),
            "is_dir": path.is_dir(),
            "extension": path.suffix,
            "is_executable": FileUtils.is_executable(str(path))
        }
    
    @staticmethod
    def scan_directory(directory: str, recursive: bool = True) -> List[str]:
        """
        Escanea un directorio y retorna lista de archivos.
        
        Args:
            directory: Directorio a escanear
            recursive: Si True, escanea subdirectorios
            
        Returns:
            Lista de rutas de archivos
        """
        path = Path(directory)
        files = []
        
        try:
            if recursive:
                files = [str(f) for f in path.rglob('*') if f.is_file()]
            else:
                files = [str(f) for f in path.glob('*') if f.is_file()]
        except Exception as e:
            logging.error(f"Error escaneando directorio {directory}: {e}")
        
        return files
