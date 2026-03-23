# app.py - Versión para Windows con PDFKit

from flask import Flask, render_template, request, send_file
import os
from datetime import datetime
import tempfile
import pdfkit

app = Flask(__name__)

app.config['SECRET_KEY'] = 'tu-clave-secreta-cambiala'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configurar PDFKit para Windows
# Cambia esta ruta según donde instalaste wkhtmltopdf
WKHTMLTOPDF_PATH = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'

# Verificar si existe el ejecutable
if os.path.exists(WKHTMLTOPDF_PATH):
    config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)
    print(f"✅ wkhtmltopdf encontrado en: {WKHTMLTOPDF_PATH}")
else:
    print(f"⚠️ No se encontró wkhtmltopdf en: {WKHTMLTOPDF_PATH}")
    print("Usando configuración por defecto (puede fallar)")
    config = pdfkit.configuration()

options = {
    'enable-local-file-access': None,
    'quiet': '',
    'print-media-type': None,
    'margin-top': '0.5cm',
    'margin-right': '0.5cm',
    'margin-bottom': '0.5cm',
    'margin-left': '0.5cm',
}

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    try:
        print("Iniciando generación de PDF con PDFKit...")
        
        datos_formulario = request.form.to_dict()
        datos_formulario['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        base_url = request.host_url.rstrip('/')
        
        html_para_pdf = render_template('plantilla_pdf.html', 
                                        datos=datos_formulario,
                                        base_url=base_url)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            pdfkit.from_string(html_para_pdf, tmp_file.name, 
                              configuration=config, 
                              options=options)
            tmp_path = tmp_file.name
        
        print(f"✅ PDF generado correctamente")
        
        nombre_operador = datos_formulario.get('operador', 'sin_operador').replace(' ', '_')
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"checklist_{nombre_operador}_{fecha_actual}.pdf"
        
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