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

    resultados = ejecutar_optimizaciones(opciones)
    return render_template('resultados.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)