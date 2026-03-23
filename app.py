# app.py - Backend para Checklist de Equipo

# Importamos las librerías necesarias
from flask import Flask, render_template, request, send_file
from weasyprint import HTML
import os
from datetime import datetime
import tempfile

# Creamos la aplicación Flask
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'tu-clave-secreta-cambiala'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Ruta principal - Muestra el formulario
@app.route('/')
def formulario():
    return render_template('formulario.html')

# Ruta para generar el PDF
@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    try:
        # 1. RECOLECTAR DATOS DEL FORMULARIO
        datos_formulario = request.form.to_dict()
        
        # Agregamos fecha y hora de generación
        datos_formulario['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. GENERAR EL PDF
        html_para_pdf = render_template('plantilla_pdf.html', datos=datos_formulario)
        
        # Convertimos el HTML a PDF usando WeasyPrint
        pdf = HTML(string=html_para_pdf).write_pdf()
        
        # 3. PREPARAR EL ARCHIVO PARA DESCARGA
        nombre_operador = datos_formulario.get('operador', 'sin_operador').replace(' ', '_')
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"checklist_{nombre_operador}_{fecha_actual}.pdf"
        
        # Guardamos temporalmente el PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf)
            tmp_path = tmp_file.name
        
        # Enviamos el PDF al usuario
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        return f"Error al generar el PDF: {str(e)}", 500

# Ruta de prueba
@app.route('/health')
def health():
    return "Servidor funcionando correctamente!", 200

# Este bloque se ejecuta solo si corres el archivo directamente
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)