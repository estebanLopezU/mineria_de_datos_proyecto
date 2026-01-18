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
        # Intentar con PowerShell primero (funciona para usuario actual sin admin)
        result = subprocess.run(['powershell', '-Command', 'Clear-RecycleBin -Force -Confirm:$false'], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return {"exito": True, "mensaje": "Papelera vaciada exitosamente con PowerShell."}
        else:
            # Fallback al comando rd tradicional
            result2 = subprocess.run(['cmd', '/c', 'rd /s /q %systemdrive%\\$Recycle.bin 2>nul'], capture_output=True, text=True)
            if result2.returncode == 0:
                return {"exito": True, "mensaje": "Papelera vaciada exitosamente."}
            else:
                return {"exito": False, "mensaje": "Error: No se pudo vaciar la papelera. Ejecuta la aplicación como administrador para esta función."}
    except subprocess.TimeoutExpired:
        return {"exito": False, "mensaje": "Operación tomó demasiado tiempo."}
    except Exception as e:
        return {"exito": False, "mensaje": f"Error: {str(e)}. Puede requerir permisos de administrador."}

def obtener_programas_inicio():
    """Obtiene lista de programas de inicio."""
    startup_path = os.path.expanduser("~\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup")
    programas = []
    if os.path.exists(startup_path):
        for item in os.listdir(startup_path):
            if item != "desktop.ini":
                programas.append(item)
    return programas

def desfragmentar_disco():
    """Desfragmenta el disco C:."""
    try:
        result = subprocess.run(['defrag', 'C:', '/O'], capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            return {"exito": True, "mensaje": "Desfragmentación completada."}
        else:
            return {"exito": False, "mensaje": f"Error en desfragmentación: {result.stderr}"}
    except subprocess.TimeoutExpired:
        return {"exito": False, "mensaje": "Desfragmentación tomó demasiado tiempo."}
    except Exception as e:
        return {"exito": False, "mensaje": str(e)}

def limpiar_prefetch():
    """Limpia archivos prefetch."""
    prefetch_path = "C:\\Windows\\Prefetch"
    eliminados = 0
    errores = 0
    if os.path.exists(prefetch_path):
        try:
            for filename in os.listdir(prefetch_path):
                if filename.endswith('.pf'):
                    file_path = os.path.join(prefetch_path, filename)
                    try:
                        os.unlink(file_path)
                        eliminados += 1
                    except Exception:
                        errores += 1
        except Exception:
            pass
    return {"eliminados": eliminados, "errores": errores}

def limpiar_cache_navegadores():
    """Limpia cache de navegadores comunes."""
    resultados = {}
    # Chrome
    chrome_cache = os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache")
    if os.path.exists(chrome_cache):
        try:
            shutil.rmtree(chrome_cache)
            resultados["chrome"] = "Cache de Chrome limpiado."
        except Exception as e:
            resultados["chrome"] = f"Error limpiando Chrome: {str(e)}"
    else:
        resultados["chrome"] = "Chrome no encontrado."

    # Firefox
    firefox_profile = os.path.expanduser("~\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles")
    if os.path.exists(firefox_profile):
        for profile in os.listdir(firefox_profile):
            cache_path = os.path.join(firefox_profile, profile, "cache2")
            if os.path.exists(cache_path):
                try:
                    shutil.rmtree(cache_path)
                    resultados["firefox"] = "Cache de Firefox limpiado."
                    break
                except Exception as e:
                    resultados["firefox"] = f"Error limpiando Firefox: {str(e)}"
                    break
        else:
            resultados["firefox"] = "Firefox no encontrado."
    else:
        resultados["firefox"] = "Firefox no encontrado."

    return resultados

def limpiar_actualizaciones_windows():
    """Limpia archivos temporales de Windows Update."""
    try:
        result = subprocess.run(['cleanmgr', '/sagerun:1'], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            return {"exito": True, "mensaje": "Limpieza de Windows Update completada."}
        else:
            return {"exito": False, "mensaje": "Error en limpieza de Windows Update."}
    except subprocess.TimeoutExpired:
        return {"exito": False, "mensaje": "Limpieza tomó demasiado tiempo."}
    except Exception as e:
        return {"exito": False, "mensaje": str(e)}

def obtener_espacio_liberado():
    """Calcula espacio liberado (estimado)."""
    # Esto es una estimación simple
    return {"espacio_estimado": "Variable según archivos eliminados"}

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
    if "desfragmentar" in opciones:
        resultados["desfragmentar"] = desfragmentar_disco()
    if "limpiar_prefetch" in opciones:
        resultados["limpiar_prefetch"] = limpiar_prefetch()
    if "limpiar_cache_nav" in opciones:
        resultados["limpiar_cache_nav"] = limpiar_cache_navegadores()
    if "limpiar_windows_update" in opciones:
        resultados["limpiar_windows_update"] = limpiar_actualizaciones_windows()
    if "espacio_liberado" in opciones:
        resultados["espacio_liberado"] = obtener_espacio_liberado()
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
    # Iniciar la aplicación web automáticamente
    from app import app
    import webbrowser
    import threading
    import time

    def open_browser():
        time.sleep(1.5)  # Esperar a que el servidor inicie
        webbrowser.open('http://127.0.0.1:5000/')

    # Iniciar hilo para abrir navegador
    threading.Thread(target=open_browser, daemon=True).start()
    # Ejecutar la aplicación web
    app.run(debug=True, host='0.0.0.0', port=5000)
