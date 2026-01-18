from flask import Flask, render_template, request
from main import ejecutar_optimizaciones

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    app.run(debug=True)