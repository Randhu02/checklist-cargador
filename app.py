# app.py - Versión optimizada

from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
import tempfile

try:
    from weasyprint import HTML
    print("WeasyPrint importado correctamente")
except ImportError:
    print("Error: WeasyPrint no está instalado")

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tu-clave-secreta-cambiala'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    try:
        print("Iniciando generación de PDF...")
        
        # Recolectar datos
        datos_formulario = request.form.to_dict()
        datos_formulario['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Obtener URL base
        base_url = request.host_url.rstrip('/')
        print(f"Base URL: {base_url}")
        
        # Generar HTML
        html_para_pdf = render_template('plantilla_pdf.html', 
                                        datos=datos_formulario,
                                        base_url=base_url)
        
        print(f"HTML generado, longitud: {len(html_para_pdf)}")
        
        # OPTIMIZACIÓN: Usar string directamente en lugar de archivo temporal
        pdf = HTML(string=html_para_pdf).write_pdf()
        print(f"PDF generado, tamaño: {len(pdf)} bytes")
        
        # Preparar archivo para descarga
        nombre_operador = datos_formulario.get('operador', 'sin_operador').replace(' ', '_')
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"checklist_{nombre_operador}_{fecha_actual}.pdf"
        
        # Guardar temporalmente para enviar
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf)
            tmp_path = tmp_file.name
        
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

@app.route('/health')
def health():
    return "Servidor funcionando correctamente!", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)