import os
import sys
import logging
from pathlib import Path

# Configurar el logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger.info(f"Python path: {sys.path}")

from flask import Flask, send_from_directory, jsonify, request, session
from flask_cors import CORS

# Configuración de la aplicación
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Configurar CORS para permitir solicitudes desde cualquier origen
CORS(app, 
     supports_credentials=True,
     resources={
         r"/api/*": {
             "origins": ["https://prueba-hero.vercel.app", "http://localhost:5000"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type", "X-CSRFToken"],
             "supports_credentials": True
         }
     })

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Para depuración de consultas SQL

# Configuración de sesión
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600  # 1 hora
)

# Importar modelos y blueprints después de configurar la aplicación
from src.models.user import db
from src.models.plato import Plato
from src.routes.user import user_bp
from src.routes.platos import platos_bp

# Inicializar la base de datos
db.init_app(app)

# Crear tablas si no existen
with app.app_context():
    try:
        db.create_all()
        logger.info("Base de datos inicializada correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar la base de datos: {str(e)}")
        raise

# Registrar blueprints con prefijos específicos
app.register_blueprint(user_bp, url_prefix='/api')
# Asegurarse de que el prefijo coincida con las rutas en el frontend
app.register_blueprint(platos_bp, url_prefix='/api')

# Ruta para servir archivos subidos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    return send_from_directory(upload_folder, filename)

# Manejador de errores para 404
@app.errorhandler(404)
def not_found_error(error):
    logger.error(f'Error 404: {error}')
    return jsonify({'error': 'Recurso no encontrado'}), 404

# Manejador de errores para 500
@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Error 500: {error}')
    return jsonify({'error': 'Error interno del servidor'}), 500

# Ruta de verificación de salud
@app.route('/health')
def health_check():
    return jsonify({'status': 'ok', 'message': 'La aplicación está en funcionamiento'})

# Ruta para la página principal
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Ruta para archivos estáticos
@app.route('/<path:path>')
def static_files(path):
    # Si la ruta comienza con 'api/', manejarla con los blueprints
    if path.startswith('api/'):
        return ''  # Las rutas de la API serán manejadas por los blueprints
    
    # Si es un archivo estático, servirlo
    static_folder_path = app.static_folder
    if static_folder_path and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    
    # Si no se encuentra el archivo, devolver 404
    return "Archivo no encontrado", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
