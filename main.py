"""
FIREGUARD AI - Sistema de Antivirus Principal

Este es el punto de entrada principal del sistema FIREGUARD AI.
Carga la configuración, inicializa todos los módulos y coordina
la ejecución del antivirus.

Uso:
    python main.py [--config CONFIG_PATH]
"""

import sys
import argparse
import logging
from pathlib import Path

from fireguard.core import FireguardEngine
from fireguard.utils import ConfigLoader, setup_logger


def parse_arguments():
    """
    Procesa los argumentos de línea de comandos.
    
    Returns:
        Namespace con los argumentos procesados
    """
    parser = argparse.ArgumentParser(
        description='FIREGUARD AI - Sistema de Antivirus Multiplataforma'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config.yaml',
        help='Ruta al archivo de configuración (default: config.yaml)'
    )
    
    parser.add_argument(
        '--log-level',
        type=str,
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        default='INFO',
        help='Nivel de logging (default: INFO)'
    )
    
    parser.add_argument(
        '--log-file',
        type=str,
        default=None,
        help='Archivo de log opcional'
    )
    
    return parser.parse_args()


def load_configuration(config_path: str) -> dict:
    """
    Carga la configuración del sistema.
    
    Args:
        config_path: Ruta al archivo de configuración
        
    Returns:
        Diccionario con la configuración cargada
    """
    config_loader = ConfigLoader()
    
    try:
        config = config_loader.load_from_file(config_path)
        return config
    except FileNotFoundError:
        # Si no existe el archivo, usar configuración por defecto
        print(f"Advertencia: Archivo de configuración no encontrado: {config_path}")
        print("Usando configuración por defecto")
        return get_default_config()
    except Exception as e:
        print(f"Error al cargar configuración: {e}")
        sys.exit(1)


def get_default_config() -> dict:
    """
    Retorna la configuración por defecto del sistema.
    
    Returns:
        Diccionario con configuración por defecto
    """
    return {
        "system": {
            "name": "FIREGUARD AI",
            "version": "0.1.0",
            "platform": "multi"
        },
        "logging": {
            "level": "INFO",
            "file": "logs/fireguard.log",
            "console": True
        },
        "sensors": {
            "port_monitor": {
                "enabled": True,
                "monitored_ports": [80, 443, 22, 21, 3389]
            },
            "log_analyzer": {
                "enabled": True,
                "log_paths": []
            }
        },
        "alerts": {
            "channels": ["console", "log"],
            "recipients": []
        },
        "auth": {
            "enabled": False,
            "require_login": False
        }
    }


def main():
    """
    Función principal del sistema FIREGUARD AI.
    
    Coordina la inicialización y ejecución del antivirus.
    """
    # Parsear argumentos
    args = parse_arguments()
    
    # Configurar logging
    log_level = getattr(logging, args.log_level)
    logger = setup_logger(
        name="fireguard",
        level=log_level,
        log_file=args.log_file,
        console=True
    )
    
    logger.info("="*60)
    logger.info("FIREGUARD AI - Sistema de Antivirus")
    logger.info("="*60)
    
    # Cargar configuración
    logger.info(f"Cargando configuración desde: {args.config}")
    config = load_configuration(args.config)
    
    logger.info(f"Sistema: {config.get('system', {}).get('name', 'FIREGUARD AI')}")
    logger.info(f"Versión: {config.get('system', {}).get('version', '0.1.0')}")
    
    # Inicializar el motor del antivirus
    try:
        logger.info("Inicializando motor del antivirus...")
        engine = FireguardEngine(config)
        
        # Iniciar el motor
        if engine.start():
            logger.info("Motor iniciado exitosamente")
            
            # Mostrar estado
            status = engine.status()
            logger.info(f"Estado del sistema: {status}")
            
            # Mensaje de sistema listo
            logger.info("="*60)
            logger.info("FIREGUARD AI está listo y protegiendo el sistema")
            logger.info("Presiona Ctrl+C para detener")
            logger.info("="*60)
            
            # Mantener el programa ejecutándose
            try:
                import time
                while engine.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("\nSeñal de interrupción recibida")
            
            # Detener el motor
            logger.info("Deteniendo el motor del antivirus...")
            engine.stop()
            logger.info("FIREGUARD AI detenido correctamente")
        
        else:
            logger.error("Error al iniciar el motor del antivirus")
            sys.exit(1)
    
    except Exception as e:
        logger.exception(f"Error fatal en FIREGUARD AI: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
