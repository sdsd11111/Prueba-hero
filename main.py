import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from src.models.user import db
from src.models.plato import Plato
from src.routes.user import user_bp
from src.routes.platos import platos_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Registrar blueprints con prefijos específicos
app.register_blueprint(user_bp, url_prefix='/api')
# Asegurarse de que el prefijo coincida con las rutas en el frontend
app.register_blueprint(platos_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    upload_folder = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    return send_from_directory(upload_folder, filename)

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
