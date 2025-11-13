#!/usr/bin/env python3
"""
Script de configuración para la calculadora web.
"""
import os
import sys
import subprocess

def run_command(command):
    """Ejecuta un comando y maneja errores."""
    try:
        result = subprocess.run(command, shell=True, check=True, 
                              capture_output=True, text=True)
        print(f"✓ {command}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {command}")
        print(f"Error: {e.stderr}")
        return False

def main():
    print("Configurando Calculadora Web...")
    print("=" * 40)
    
    # Verificar Python
    if not run_command("python --version"):
        sys.exit(1)
    
    # Crear estructura de directorios si no existe
    directories = ['calculadora', 'pruebas', 'static', 'templates']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✓ Directorio creado: {directory}")
    
    # Instalar dependencias de desarrollo
    dependencies = [
        "pip install --upgrade pip",
        "pip install pylint",
        "pip install bandit",
        "pip install unittest-xml-reporting"
    ]
    
    print("\nInstalando dependencias de desarrollo...")
    for dep in dependencies:
        if not run_command(dep):
            print("Advertencia: Algunas dependencias no se instalaron correctamente")
    
    print("\n" + "=" * 40)
    print("Configuración completada!")
    print("\nComandos disponibles:")
    print("  python app.py                    - Iniciar servidor")
    print("  python -m unittest discover -v   - Ejecutar pruebas")
    print("  pylint calculadora/              - Análisis de código")
    print("  bandit -r calculadora/           - Análisis de seguridad")

if __name__ == "__main__":
    main()
