"""
FIREGUARD AI - CLI Principal
Interfaz de línea de comandos para el sistema FIREGUARD
"""

import click
import json
from colorama import init, Fore, Style
from fireguard import __version__
from fireguard.core.platform_detector import PlatformDetector
from fireguard.core.config_manager import ConfigManager
from fireguard.core.logger import Logger
from fireguard.auth.auth_manager import AuthManager
from fireguard.sensors.port_sensor import PortSensor
from fireguard.sensors.process_sensor import ProcessSensor
from fireguard.sensors.disk_sensor import DiskSensor
from fireguard.sensors.log_sensor import LogSensor
from fireguard.ai.anomaly_detector import AnomalyDetector
from fireguard.ai.alert_system import AlertSystem

# Inicializar colorama para colores en terminal
init(autoreset=True)


@click.group()
@click.version_option(version=__version__)
def cli():
    """
    🔥 FIREGUARD AI - Sistema Modular de Vigilancia y Seguridad
    
    Sistema multiplataforma para monitoreo de seguridad con capacidades de IA.
    """
    pass


@cli.command()
def info():
    """Muestra información del sistema y plataforma"""
    click.echo(f"{Fore.CYAN}{'='*60}")
    click.echo(f"{Fore.GREEN}🔥 FIREGUARD AI v{__version__}")
    click.echo(f"{Fore.CYAN}{'='*60}\n")
    
    # Información de plataforma
    platform = PlatformDetector()
    platform_info = platform.get_info()
    
    click.echo(f"{Fore.YELLOW}Plataforma:")
    click.echo(f"  Sistema: {Fore.WHITE}{platform_info['platform_type']}")
    click.echo(f"  Release: {Fore.WHITE}{platform_info['details']['release']}")
    click.echo(f"  Arquitectura: {Fore.WHITE}{platform_info['details']['machine']}")
    click.echo(f"  Python: {Fore.WHITE}{platform_info['details']['python_version']}\n")
    
    click.echo(f"{Fore.YELLOW}Características soportadas:")
    for feature, supported in platform_info['features'].items():
        status = f"{Fore.GREEN}✓" if supported else f"{Fore.RED}✗"
        click.echo(f"  {status} {feature}")
    
    click.echo()


@cli.command()
@click.option('--sensor', '-s', type=click.Choice(['ports', 'processes', 'disk', 'logs', 'all']), default='all', help='Sensor a escanear')
@click.option('--format', '-f', type=click.Choice(['text', 'json']), default='text', help='Formato de salida')
def scan(sensor, format):
    """Ejecuta un escaneo de seguridad"""
    logger = Logger()
    config = ConfigManager()
    alert_system = AlertSystem(config)
    
    click.echo(f"{Fore.CYAN}🔍 Iniciando escaneo de seguridad...\n")
    
    sensors_to_run = []
    
    if sensor == 'all' or sensor == 'ports':
        sensors_to_run.append(PortSensor(config))
    if sensor == 'all' or sensor == 'processes':
        sensors_to_run.append(ProcessSensor(config))
    if sensor == 'all' or sensor == 'disk':
        sensors_to_run.append(DiskSensor(config))
    if sensor == 'all' or sensor == 'logs':
        sensors_to_run.append(LogSensor(config))
    
    results = []
    
    for s in sensors_to_run:
        result = s.run()
        results.append(result)
        
        # Añadir alertas al sistema
        if 'alerts' in result:
            alert_system.add_alerts(result['alerts'])
    
    # Mostrar resultados
    if format == 'json':
        click.echo(json.dumps(results, indent=2))
    else:
        _display_scan_results(results, alert_system)


def _display_scan_results(results, alert_system):
    """Muestra resultados del escaneo en formato texto"""
    for result in results:
        sensor_name = result.get('sensor', 'Unknown')
        status = result.get('status', 'unknown')
        
        if status == 'success':
            click.echo(f"{Fore.GREEN}✓ {sensor_name}")
            
            alert_count = result.get('alert_count', 0)
            if alert_count > 0:
                click.echo(f"  {Fore.YELLOW}⚠ {alert_count} alerta(s) detectada(s)")
                
                for alert in result.get('alerts', [])[:3]:  # Mostrar máximo 3 alertas
                    severity = alert.get('severity', 'unknown')
                    message = alert.get('message', 'Sin mensaje')
                    
                    color = Fore.RED if severity in ['critical', 'high'] else Fore.YELLOW
                    click.echo(f"    {color}• [{severity.upper()}] {message}")
            else:
                click.echo(f"  {Fore.GREEN}✓ Sin alertas")
        else:
            click.echo(f"{Fore.RED}✗ {sensor_name} - Error: {result.get('error', 'Unknown')}")
        
        click.echo()
    
    # Resumen de alertas
    summary = alert_system.get_alert_summary()
    if summary['total'] > 0:
        click.echo(f"{Fore.CYAN}{'='*60}")
        click.echo(f"{Fore.YELLOW}📊 Resumen de Alertas:")
        click.echo(f"  Total: {Fore.WHITE}{summary['total']}")
        
        if summary['by_severity']:
            click.echo(f"  Por severidad:")
            for sev, count in summary['by_severity'].items():
                color = Fore.RED if sev in ['critical', 'high'] else Fore.YELLOW
                click.echo(f"    {color}{sev}: {count}")


@cli.command()
def auth():
    """Gestiona la autenticación de usuarios"""
    click.echo(f"{Fore.CYAN}🔐 Sistema de Autenticación FIREGUARD\n")
    
    auth_manager = AuthManager()
    
    click.echo("Métodos disponibles:")
    click.echo("  1. Autenticación Local")
    click.echo("  2. GitHub OAuth (requiere configuración)")
    click.echo("  3. Google OAuth (requiere configuración)")
    
    choice = click.prompt("\nSeleccione método", type=int, default=1)
    
    if choice == 1:
        username = click.prompt("Usuario")
        password = click.prompt("Contraseña", hide_input=True)
        
        token = auth_manager.authenticate_local(username, password)
        
        if token:
            click.echo(f"\n{Fore.GREEN}✓ Autenticación exitosa!")
            click.echo(f"Token: {Fore.WHITE}{token}")
        else:
            click.echo(f"\n{Fore.RED}✗ Autenticación fallida")
    else:
        click.echo(f"\n{Fore.YELLOW}OAuth requiere configuración adicional.")
        click.echo("Consulte la documentación para más información.")


@cli.command()
@click.option('--output', '-o', type=click.Path(), help='Archivo de salida para el reporte')
def report(output):
    """Genera un reporte completo del sistema"""
    click.echo(f"{Fore.CYAN}📋 Generando reporte completo...\n")
    
    config = ConfigManager()
    platform = PlatformDetector()
    alert_system = AlertSystem(config)
    
    # Ejecutar todos los sensores
    sensors = [
        PortSensor(config),
        ProcessSensor(config),
        DiskSensor(config),
        LogSensor(config),
    ]
    
    report_data = {
        "timestamp": click.DateTime().now().isoformat(),
        "version": __version__,
        "platform": platform.get_info(),
        "sensors": []
    }
    
    for sensor in sensors:
        result = sensor.run()
        report_data["sensors"].append(result)
        
        if 'alerts' in result:
            alert_system.add_alerts(result['alerts'])
    
    report_data["alert_summary"] = alert_system.get_alert_summary()
    
    # Guardar o mostrar reporte
    report_json = json.dumps(report_data, indent=2)
    
    if output:
        with open(output, 'w') as f:
            f.write(report_json)
        click.echo(f"{Fore.GREEN}✓ Reporte guardado en: {output}")
    else:
        click.echo(report_json)


@cli.command()
def config():
    """Muestra la configuración actual"""
    click.echo(f"{Fore.CYAN}⚙️ Configuración FIREGUARD\n")
    
    config_mgr = ConfigManager()
    config_data = config_mgr.get_all()
    
    click.echo(json.dumps(config_data, indent=2))


if __name__ == '__main__':
    cli()
