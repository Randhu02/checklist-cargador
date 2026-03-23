# app.py - Backend para Checklist de Equipo

# Importamos las librerías necesarias
from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
import tempfile

# Intentamos importar WeasyPrint
try:
    from weasyprint import HTML
    print("WeasyPrint importado correctamente")
except ImportError:
    print("Error: WeasyPrint no está instalado")

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
        print("Iniciando generación de PDF...")
        
        # 1. RECOLECTAR DATOS DEL FORMULARIO
        datos_formulario = request.form.to_dict()
        print(f"Datos recibidos: {datos_formulario.keys()}")
        
        # Agregamos fecha y hora de generación
        datos_formulario['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. GENERAR EL PDF - MÉTODO ALTERNATIVO
        html_para_pdf = render_template('plantilla_pdf.html', datos=datos_formulario)
        
        # Guardar el HTML temporalmente para debug
        print("HTML generado, longitud:", len(html_para_pdf))
        
        # Método alternativo: crear PDF desde archivo temporal
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
            f.write(html_para_pdf)
            temp_html_path = f.name
        
        print(f"HTML temporal guardado en: {temp_html_path}")
        
        # Convertir HTML a PDF
        pdf = HTML(filename=temp_html_path).write_pdf()
        print(f"PDF generado, tamaño: {len(pdf)} bytes")
        
        # Limpiar archivo temporal
        os.unlink(temp_html_path)
        
        # 3. PREPARAR EL ARCHIVO PARA DESCARGA
        nombre_operador = datos_formulario.get('operador', 'sin_operador').replace(' ', '_')
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"checklist_{nombre_operador}_{fecha_actual}.pdf"
        
        # Guardamos temporalmente el PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf)
            tmp_path = tmp_file.name
        
        print(f"PDF guardado en: {tmp_path}")
        
        # Enviamos el PDF al usuario
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return f"Error al generar el PDF: {str(e)}", 500

# Ruta de prueba
@app.route('/health')
def health():
    return "Servidor funcionando correctamente!", 200

# Este bloque se ejecuta solo si corres el archivo directamente
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)