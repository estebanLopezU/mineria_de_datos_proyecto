from flask import Flask, render_template, request, jsonify
from main import ejecutar_optimizaciones, obtener_info_sistema
import psutil
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    opciones = []
    if request.form.get('info_sistema'):
        opciones.append('info_sistema')
    if request.form.get('limpiar_temp'):
        opciones.append('limpiar_temp')
    if request.form.get('vaciar_papelera'):
        opciones.append('vaciar_papelera')
    if request.form.get('listar_inicio'):
        opciones.append('listar_inicio')
    if request.form.get('desfragmentar'):
        opciones.append('desfragmentar')
    if request.form.get('limpiar_prefetch'):
        opciones.append('limpiar_prefetch')
    if request.form.get('limpiar_cache_nav'):
        opciones.append('limpiar_cache_nav')
    if request.form.get('limpiar_windows_update'):
        opciones.append('limpiar_windows_update')
    if request.form.get('espacio_liberado'):
        opciones.append('espacio_liberado')

    resultados = ejecutar_optimizaciones(opciones)
    return render_template('resultados.html', resultados=resultados)

@app.route('/api/system_stats')
def system_stats():
    """API endpoint para estadísticas del sistema en tiempo real"""
    try:
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()

        # Memoria
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        memory_used = memory.used / (1024**3)  # GB
        memory_total = memory.total / (1024**3)  # GB

        # Disco
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        disk_used = disk.used / (1024**3)  # GB
        disk_total = disk.total / (1024**3)  # GB

        # Red
        net = psutil.net_io_counters()
        net_sent = net.bytes_sent / (1024**2)  # MB
        net_recv = net.bytes_recv / (1024**2)  # MB

        # Procesos
        process_count = len(psutil.pids())

        return jsonify({
            'timestamp': time.time(),
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count,
                'freq_current': cpu_freq.current if cpu_freq else 0,
                'freq_max': cpu_freq.max if cpu_freq else 0
            },
            'memory': {
                'percent': memory_percent,
                'used': round(memory_used, 2),
                'total': round(memory_total, 2)
            },
            'disk': {
                'percent': disk_percent,
                'used': round(disk_used, 2),
                'total': round(disk_total, 2)
            },
            'network': {
                'sent': round(net_sent, 2),
                'recv': round(net_recv, 2)
            },
            'processes': process_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)