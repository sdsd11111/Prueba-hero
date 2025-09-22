import os
import sys
import logging
from datetime import timedelta
from pathlib import Path

# Configurar el logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)

# Asegurarse de que el directorio raíz esté en el path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_path)
logger.info(f"Python path: {sys.path}")

from flask import Flask, send_from_directory, jsonify, request, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# Inicializar la base de datos
db = SQLAlchemy()

# Configuración de la aplicación
app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configuración de la aplicación
app.config.update(
    SECRET_KEY=os.environ.get('FLASK_SECRET_KEY', 'asdf#FGSgvasgf$5$WGT'),
    SESSION_COOKIE_NAME='prueba_hero_session',
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,  # Solo enviar cookies a través de HTTPS
    SESSION_COOKIE_SAMESITE='None',  # Necesario para CORS con credenciales
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24),  # La sesión expira después de 24 horas
    SESSION_REFRESH_EACH_REQUEST=True,
    SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}",
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_ECHO=True,  # Para depuración de consultas SQL
    PROPAGATE_EXCEPTIONS=True
)

# Inicializar la base de datos con la aplicación
db.init_app(app)

# Configurar CORS
CORS(
    app,
    resources={
        r"/api/*": {
            "origins": ["https://prueba-hero.vercel.app", "http://localhost:3000", "http://localhost:5000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "Accept"],
            "supports_credentials": True,
            "expose_headers": ["Content-Type", "Set-Cookie", "Authorization"],
            "max_age": 600
        }
    }
)

# Crear directorio de base de datos si no existe
db_dir = os.path.join(os.path.dirname(__file__), 'database')
os.makedirs(db_dir, exist_ok=True)

# Importar modelos y blueprints después de configurar la aplicación
from src.models.user import db as user_db
from src.models.plato import Plato, db as plato_db
from src.routes.user import user_bp
from src.routes.platos import platos_bp

# Inicializar la base de datos con la aplicación
user_db.init_app(app)
plato_db.init_app(app)

# Registrar blueprints con prefijos específicos
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(platos_bp, url_prefix='/api')

# Crear tablas de la base de datos
with app.app_context():
    try:
        # Crear todas las tablas
        user_db.create_all()
        plato_db.create_all()
        logger.info("Bases de datos inicializadas correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar las bases de datos: {e}")
        raise

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
