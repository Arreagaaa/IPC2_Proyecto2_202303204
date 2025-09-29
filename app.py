from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for, send_from_directory
import os
import tempfile
import zipfile
from werkzeug.utils import secure_filename
from app.controllers.sistema_riego import SistemaRiego
from app.tdas.lista_enlazada import ListaEnlazada


app = Flask(__name__)
app.secret_key = 'guateriegos_2025_secret_key'

# configuracion de subida de archivos
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# crear directorio de uploads si no existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('static/reports', exist_ok=True)
os.makedirs('static/graphs', exist_ok=True)
os.makedirs('output', exist_ok=True)

# sistema global
sistema = SistemaRiego()


def allowed_file(filename):
    # verificar si el archivo tiene extension permitida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    # pagina principal
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    # cargar archivo XML de configuracion
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No se seleccionó archivo', 'error')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No se seleccionó archivo', 'error')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # cargar configuracion en el sistema
            success = sistema.cargar_configuracion(filepath)
            if success:
                flash('Archivo cargado exitosamente', 'success')
                return redirect(url_for('simulation'))
            else:
                flash('Error al procesar el archivo XML', 'error')
        else:
            flash('Tipo de archivo no permitido. Solo archivos .xml', 'error')

    return render_template('upload.html')


@app.route('/simulation')
def simulation():
    # pagina de simulacion y seleccion
    if sistema.invernaderos.obtener_tamaño() == 0:
        flash('Primero debe cargar un archivo de configuración', 'warning')
        return redirect(url_for('upload_file'))

    # obtener lista de invernaderos usando TDA
    invernaderos_data = ListaEnlazada()
    for i in range(sistema.invernaderos.obtener_tamaño()):
        inv = sistema.invernaderos.obtener(i)

        # obtener planes de riego usando TDA
        planes_data = ListaEnlazada()
        plan_original = inv.plan_riego.obtener_plan_original()
        if plan_original:
            planes_data.insertar_al_final({
                'nombre': 'Plan Principal',
                'secuencia': plan_original
            })

        # convertir planes_data a lista nativa solo para template
        planes_list = []
        for plan in planes_data:
            planes_list.append(plan)

        invernaderos_data.insertar_al_final({
            'nombre': inv.nombre,
            'hileras': inv.hileras.obtener_tamaño(),
            'drones': inv.drones.obtener_tamaño(),
            'plantas_total': sum(inv.hileras.obtener(j).plantas.obtener_tamaño()
                                 for j in range(inv.hileras.obtener_tamaño())),
            'planes': planes_list
        })

    # convertir a lista nativa solo para template
    invernaderos_list = []
    for inv in invernaderos_data:
        invernaderos_list.append(inv)

    return render_template('simulation.html', invernaderos=invernaderos_list)


@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    # ejecutar simulacion para invernadero seleccionado
    data = request.get_json()
    invernadero_nombre = data.get('invernadero')

    if not invernadero_nombre:
        return jsonify({'error': 'Debe seleccionar un invernadero'}), 400

    # buscar y seleccionar invernadero
    invernadero_encontrado = None
    for i in range(sistema.invernaderos.obtener_tamaño()):
        inv = sistema.invernaderos.obtener(i)
        if inv.nombre == invernadero_nombre:
            invernadero_encontrado = inv
            break

    if not invernadero_encontrado:
        return jsonify({'error': 'Invernadero no encontrado'}), 404

    # establecer invernadero actual y ejecutar simulacion
    sistema.invernadero_actual = invernadero_encontrado
    success = sistema.ejecutar_simulacion()

    if not success:
        return jsonify({'error': 'Error al ejecutar la simulación'}), 500

    # obtener resultados
    ultima_simulacion = sistema.simulaciones.obtener(
        sistema.simulaciones.obtener_tamaño() - 1)
    resultados = ultima_simulacion.obtener_resultados()

    # preparar datos de respuesta usando TDA
    resultados_drones_tda = ListaEnlazada()
    for i in range(resultados.resultados_drones.obtener_tamaño()):
        dron_resultado = resultados.resultados_drones.obtener(i)
        resultados_drones_tda.insertar_al_final({
            'id': dron_resultado.id,
            'agua': dron_resultado.agua_utilizada,
            'fertilizante': dron_resultado.fertilizante_utilizado
        })

    # convertir a lista nativa solo para JSON
    resultados_drones_list = []
    for resultado in resultados_drones_tda:
        resultados_drones_list.append(resultado)

    estadisticas = {
        'tiempo_total': resultados.tiempo_total,
        'agua_total': resultados.total_agua,
        'fertilizante_total': resultados.total_fertilizante,
        'plan_ejecutado': resultados.plan_ejecutado,
        'resultados_drones': resultados_drones_list
    }

    return jsonify({
        'success': True,
        'estadisticas': estadisticas
    })


@app.route('/generate_html_report', methods=['POST'])
def generate_html_report():
    # generar reporte HTML
    if sistema.simulaciones.obtener_tamaño() == 0:
        return jsonify({'error': 'No hay simulaciones ejecutadas'}), 400

    # generar reporte usando estructura organizada
    success = sistema.generar_reporte_html()

    if success:
        nombre_invernadero = sistema.invernadero_actual.nombre.replace(
            ' ', '_')
        report_path = f"output/{nombre_invernadero}/ReporteInvernadero_{nombre_invernadero}.html"
        return jsonify({
            'success': True,
            'report_url': f"/{report_path}"
        })
    else:
        return jsonify({'error': 'Error al generar el reporte'}), 500


@app.route('/generate_tda_graph', methods=['POST'])
def generate_tda_graph():
    # generar grafico de TDAs en tiempo t con PNG y HTML
    data = request.get_json()
    tiempo_t = data.get('tiempo', 1)

    if sistema.simulaciones.obtener_tamaño() == 0:
        return jsonify({'error': 'No hay simulaciones ejecutadas'}), 400

    try:
        tiempo_t = int(tiempo_t)
        if tiempo_t < 1:
            tiempo_t = 1
    except:
        tiempo_t = 1

    # generar visualización completa para tiempo t
    success = sistema.visualizar_tdas_en_tiempo(tiempo_t)

    if success:
        # nombres de archivos generados con estructura organizada
        nombre_invernadero = sistema.invernadero_actual.nombre.replace(
            ' ', '_')
        prefix = f"visualization_t{tiempo_t}"
        base_path = f"output/{nombre_invernadero}/graficos"

        return jsonify({
            'success': True,
            'visualization': {
                'plan_riego_png': f"/{base_path}/{prefix}_plan_riego.png",
                'cola_riego_png': f"/{base_path}/{prefix}_cola_riego.png",
                'drones_png': f"/{base_path}/{prefix}_drones.png",
                'tiempo_t_png': f"/{base_path}/{prefix}_tiempo_{tiempo_t}.png",
                'plan_riego_html': f"/{base_path}/{prefix}_plan_riego.html",
                'cola_riego_html': f"/{base_path}/{prefix}_cola_riego.html",
                'drones_html': f"/{base_path}/{prefix}_drones.html",
                'tiempo_t_html': f"/{base_path}/{prefix}_tiempo_{tiempo_t}.html"
            },
            'tiempo': tiempo_t
        })
    else:
        return jsonify({'error': 'Error al generar la visualización de TDAs'}), 500


@app.route('/visualize_tda/<tiempo_t>')
def visualize_tda_at_time(tiempo_t):
    # pagina de visualización de TDAs en tiempo específico
    try:
        tiempo = int(tiempo_t)
    except:
        flash('Tiempo inválido', 'error')
        return redirect(url_for('simulation'))

    if sistema.simulaciones.obtener_tamaño() == 0:
        flash('No hay simulaciones ejecutadas', 'error')
        return redirect(url_for('simulation'))

    # obtener archivos de visualización disponibles
    archivos_disponibles = sistema.obtener_archivos_visualizacion_disponibles()

    # convertir a lista para template
    archivos_list = []
    for i in range(archivos_disponibles.obtener_tamaño()):
        archivo = archivos_disponibles.obtener(i)
        if f"t{tiempo}" in archivo:
            archivos_list.append(archivo)

    return render_template('visualization.html',
                           tiempo=tiempo,
                           archivos=archivos_list,
                           invernadero=sistema.invernadero_actual.nombre if sistema.invernadero_actual else None)


@app.route('/view_tda_graph/<path:graph_path>')
def view_tda_graph(graph_path):
    # mostrar gráfico específico de TDA desde estructura organizada
    html_path = f"output/{graph_path}"

    if not os.path.exists(html_path):
        flash('Archivo de visualización no encontrado', 'error')
        return redirect(url_for('simulation'))

    # leer contenido del archivo HTML
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except Exception as e:
        flash(f'Error al cargar visualización: {e}', 'error')
        return redirect(url_for('simulation'))


@app.route('/generate_xml_output')
def generate_xml_output():
    # generar archivo XML de salida
    if sistema.simulaciones.obtener_tamaño() == 0:
        flash('No hay simulaciones ejecutadas', 'warning')
        return redirect(url_for('simulation'))

    nombre_invernadero = sistema.invernadero_actual.nombre.replace(' ', '_')
    output_path = f'output/{nombre_invernadero}/salida.xml'
    success = sistema.generar_archivo_salida(output_path)

    if success:
        return send_file(output_path, as_attachment=True, download_name='salida.xml')
    else:
        flash('Error al generar el archivo de salida', 'error')
        return redirect(url_for('simulation'))


# Función download_reports eliminada por solicitud del usuario


@app.route('/output/<path:filename>')
def serve_output_files(filename):
    # servir archivos desde la carpeta output organizada
    return send_from_directory('output', filename)


@app.route('/help')
def help_page():
    # pagina de ayuda e informacion
    return render_template('help.html')


@app.route('/api/simulation_status')
def simulation_status():
    # obtener estado actual del sistema
    status = {
        'invernaderos_cargados': sistema.invernaderos.obtener_tamaño(),
        'simulaciones_ejecutadas': sistema.simulaciones.obtener_tamaño(),
        'invernadero_actual': sistema.invernadero_actual.nombre if sistema.invernadero_actual else None
    }
    return jsonify(status)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
