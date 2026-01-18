import os
import shutil
import tempfile
import subprocess
import psutil

def obtener_info_sistema():
    """Obtiene información básica del sistema."""
    info = {
        "cpu": psutil.cpu_count(),
        "memoria": psutil.virtual_memory().total / (1024**3),
        "disco": psutil.disk_usage('/').total / (1024**3)
    }
    return info

def limpiar_archivos_temporales():
    """Limpia archivos temporales."""
    temp_dir = tempfile.gettempdir()
    eliminados = 0
    errores = 0
    try:
        for filename in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    eliminados += 1
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    eliminados += 1
            except Exception as e:
                errores += 1
    except Exception as e:
        pass
    return {"eliminados": eliminados, "errores": errores}

def vaciar_papelera():
    """Vacía la papelera de reciclaje en Windows."""
    try:
        # Comando para Windows
        result = subprocess.run(['cmd', '/c', 'rd /s /q %systemdrive%\\$Recycle.bin'], capture_output=True, text=True)
        if result.returncode == 0:
            return {"exito": True, "mensaje": "Papelera vaciada exitosamente."}
        else:
            return {"exito": False, "mensaje": f"Error: {result.stderr}"}
    except Exception as e:
        return {"exito": False, "mensaje": str(e)}

def obtener_programas_inicio():
    """Obtiene lista de programas de inicio."""
    startup_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    programas = []
    if os.path.exists(startup_path):
        for item in os.listdir(startup_path):
            if item != "desktop.ini":
                programas.append(item)
    return programas

def ejecutar_optimizaciones(opciones):
    """Ejecuta las optimizaciones seleccionadas."""
    resultados = {}
    if "info_sistema" in opciones:
        resultados["info_sistema"] = obtener_info_sistema()
    if "limpiar_temp" in opciones:
        resultados["limpiar_temp"] = limpiar_archivos_temporales()
    if "vaciar_papelera" in opciones:
        resultados["vaciar_papelera"] = vaciar_papelera()
    if "listar_inicio" in opciones:
        resultados["programas_inicio"] = obtener_programas_inicio()
    return resultados

def main():
    print("Optimizador de PC - Inicio")
    info = obtener_info_sistema()
    print(f"CPU: {info['cpu']} núcleos")
    print(f"Memoria total: {info['memoria']:.2f} GB")
    print(f"Disco total: {info['disco']:.2f} GB")
    print()

    temp = limpiar_archivos_temporales()
    print(f"Archivos temporales: {temp['eliminados']} eliminados, {temp['errores']} errores")
    print()

    papelera = vaciar_papelera()
    print(f"Papelera: {papelera['mensaje']}")
    print()

    inicio = obtener_programas_inicio()
    print("Programas de inicio:")
    for prog in inicio:
        print(f"  {prog}")
    print()

    print("Optimización completada.")

if __name__ == "__main__":
    main()
