import os
import shutil
import tempfile
import subprocess
import psutil

def obtener_info_sistema():
    """Obtiene información básica del sistema."""
    print("Información del sistema:")
    print(f"CPU: {psutil.cpu_count()} núcleos")
    print(f"Memoria total: {psutil.virtual_memory().total / (1024**3):.2f} GB")
    print(f"Disco total: {psutil.disk_usage('/').total / (1024**3):.2f} GB")
    print()

def limpiar_archivos_temporales():
    """Limpia archivos temporales."""
    temp_dir = tempfile.gettempdir()
    print(f"Limpiando archivos temporales en: {temp_dir}")
    try:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f"No se pudo eliminar {file_path}: {e}")
        print("Archivos temporales limpiados.")
    except Exception as e:
        print(f"Error al limpiar temporales: {e}")
    print()

def vaciar_papelera():
    """Vacía la papelera de reciclaje en Windows."""
    print("Vaciando papelera de reciclaje...")
    try:
        # Comando para Windows
        subprocess.run(['cmd', '/c', 'rd /s /q %systemdrive%\\$Recycle.bin'], check=True)
        print("Papelera vaciada.")
    except subprocess.CalledProcessError as e:
        print(f"Error al vaciar papelera: {e}")
    print()

def optimizar_inicio():
    """Lista programas de inicio (simplificado)."""
    print("Programas de inicio:")
    # Esto es simplificado; en un optimizador real, leería el registro
    startup_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    if os.path.exists(startup_path):
        for item in os.listdir(startup_path):
            print(f"  {item}")
    print()

def main():
    print("Optimizador de PC - Inicio")
    obtener_info_sistema()
    limpiar_archivos_temporales()
    vaciar_papelera()
    optimizar_inicio()
    print("Optimización completada.")

if __name__ == "__main__":
    main()