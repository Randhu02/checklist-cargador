# app.py - Backend para Checklist de Equipo

# Importamos las librerías necesarias
from flask import Flask, render_template, request, send_file
from flask_weasyprint import HTML, render_pdf
import os
from datetime import datetime
import tempfile

# Creamos la aplicación Flask
app = Flask(__name__)

# Configuración
app.config['SECRET_KEY'] = 'tu-clave-secreta-cambiala'  # Para seguridad
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Límite de 16MB para archivos

# Ruta principal - Muestra el formulario
@app.route('/')
def formulario():
    """
    Esta función se ejecuta cuando alguien visita la página principal
    Renderiza (muestra) el archivo formulario.html
    """
    return render_template('formulario.html')

# Ruta para generar el PDF - Procesa los datos del formulario
@app.route('/generar-pdf', methods=['POST'])
def generar_pdf():
    """
    Esta función se ejecuta cuando el usuario envía el formulario
    Toma todos los datos, los pone en la plantilla y genera el PDF
    """
    try:
        # 1. RECOLECTAR DATOS DEL FORMULARIO
        # ------------------------------------
        # request.form contiene todos los datos que envió el usuario
        datos_formulario = request.form.to_dict()
        
        # Agregamos fecha y hora de generación
        datos_formulario['fecha_generacion'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 2. PROCESAR LOS CHECKS (Bueno/Malo)
        # ------------------------------------
        # Aquí procesaremos cada sección de tu checklist
        # Por ahora es un ejemplo, luego lo expandiremos
        
        # Ejemplo de cómo capturar los radios buttons
        secciones = [
            'neumaticos', 'cilindros', 'brazos', 'debajo',
            'transmision', 'peldaños', 'combustible', 'aceite_diferencial'
        ]
        
        for seccion in secciones:
            if seccion in datos_formulario:
                # Si el valor es 'Bueno' o 'Malo'
                print(f"{seccion}: {datos_formulario[seccion]}")
        
        # 3. GENERAR EL PDF
        # ------------------------------------
        # Renderizamos la plantilla HTML con los datos
        html_para_pdf = render_template('plantilla_pdf.html', datos=datos_formulario)
        
        # Convertimos el HTML a PDF usando WeasyPrint
        pdf = HTML(string=html_para_pdf).write_pdf()
        
        # 4. PREPARAR EL ARCHIVO PARA DESCARGA
        # ------------------------------------
        # Creamos un nombre de archivo único
        nombre_operador = datos_formulario.get('operador', 'sin_operador').replace(' ', '_')
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"checklist_{nombre_operador}_{fecha_actual}.pdf"
        
        # Guardamos temporalmente el PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            tmp_file.write(pdf)
            tmp_path = tmp_file.name
        
        # Enviamos el PDF al usuario para descargar
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=nombre_archivo,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        # Si algo sale mal, mostramos el error
        return f"Error al generar el PDF: {str(e)}", 500

# Ruta de prueba para verificar que el servidor funciona
@app.route('/health')
def health():
    return "Servidor funcionando correctamente!", 200

# Este bloque se ejecuta solo si corres el archivo directamente
if __name__ == '__main__':
    # Modo debug=True para desarrollo (se actualiza solo cuando cambias código)
    # host='0.0.0.0' para que sea accesible desde otros dispositivos en tu red
    app.run(debug=True, host='0.0.0.0', port=5000)