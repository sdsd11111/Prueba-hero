from flask import Blueprint, request, jsonify, session, render_template_string, current_app
from src.models.plato import db, Plato
import os
import base64
from werkzeug.utils import secure_filename

platos_bp = Blueprint('platos', __name__)

# Credenciales de acceso
ADMIN_USERNAME = "La herencia"
ADMIN_PASSWORD = "laherencia123"

# Configuración de la carpeta de subidas
UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def ensure_upload_dir():
    # Obtener la ruta base de la aplicación
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    upload_path = os.path.abspath(os.path.join(base_dir, UPLOAD_FOLDER))
    
    print(f"Ruta base de la aplicación: {base_dir}")
    print(f"Ruta de subida calculada: {upload_path}")
    
    try:
        # Asegurarse de que el directorio exista
        if not os.path.exists(upload_path):
            print(f"Creando directorio de subidas en: {upload_path}")
            os.makedirs(upload_path, exist_ok=True)
            print(f"Directorio de subidas creado exitosamente en: {upload_path}")
        
        # Verificar permisos de escritura
        test_file = os.path.join(upload_path, 'test_permissions.txt')
        with open(test_file, 'w') as f:
            f.write('test')
@platos_bp.route('/platos', methods=['GET'])
def get_platos():
    # Si no está autenticado, devolver solo los platos activos
    if not session.get('admin_logged_in'):
        platos = Plato.query.filter_by(activo=True).order_by(Plato.orden.asc()).limit(3).all()
        return jsonify([plato.to_dict() for plato in platos])
    
    # Si está autenticado, devolver todos los platos
    platos = Plato.query.order_by(Plato.orden.asc()).all()
    return jsonify([plato.to_dict() for plato in platos])

@platos_bp.route('/platos', methods=['POST'])
def create_plato():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'No autorizado'}), 401
    
    # Verificar que no haya más de 3 platos activos
    platos_activos = Plato.query.filter_by(activo=True).count()
    if platos_activos >= 3:
        return jsonify({'error': 'No se pueden tener más de 3 platos del día activos'}), 400
    
    data = request.get_json()
    
    # Determinar el siguiente orden
    max_orden = db.session.query(db.func.max(Plato.orden)).scalar() or 0
    
    nuevo_plato = Plato(
        titulo=data['titulo'],
        descripcion=data['descripcion'],
        precio=float(data['precio']),
        imagen_url=data.get('imagen_url', ''),
        orden=max_orden + 1
    )
    
    db.session.add(nuevo_plato)
    db.session.commit()
    
    return jsonify(nuevo_plato.to_dict()), 201

@platos_bp.route('/admin/platos/<int:plato_id>', methods=['PUT'])
def update_plato(plato_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'No autorizado'}), 401
    
    plato = Plato.query.get_or_404(plato_id)
    data = request.get_json()
    
    plato.titulo = data.get('titulo', plato.titulo)
    plato.descripcion = data.get('descripcion', plato.descripcion)
    plato.precio = float(data.get('precio', plato.precio))
    plato.imagen_url = data.get('imagen_url', plato.imagen_url)
    plato.activo = data.get('activo', plato.activo)
    
    db.session.commit()
    
    return jsonify(plato.to_dict())

@platos_bp.route('/admin/platos/<int:plato_id>', methods=['DELETE'])
def delete_plato(plato_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'No autorizado'}), 401
    
    plato = Plato.query.get_or_404(plato_id)
    db.session.delete(plato)
    db.session.commit()
    
    return jsonify({'message': 'Plato eliminado exitosamente'})

@platos_bp.route('/admin/platos/<int:plato_id>/toggle', methods=['PUT'])
def toggle_plato_activo(plato_id):
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'No autorizado'}), 401
    
    plato = Plato.query.get_or_404(plato_id)
    
    # Si se está activando, verificar límite de 3
    if not plato.activo:
        platos_activos = Plato.query.filter_by(activo=True).count()
        if platos_activos >= 3:
            return jsonify({'error': 'No se pueden tener más de 3 platos del día activos'}), 400
    
    plato.activo = not plato.activo
    db.session.commit()
    
    return jsonify(plato.to_dict())

@platos_bp.route('/upload-image', methods=['POST'])
def upload_image():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'No autorizado'}), 401
    
    if 'image' not in request.files:
        return jsonify({'error': 'No se encontró archivo de imagen'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó archivo'}), 400
    
    print(f"Archivo recibido: {file.filename}")
    
    if file and allowed_file(file.filename):
        upload_path = ensure_upload_dir()
        print(f"Directorio de subida: {upload_path}")
        
        filename = secure_filename(file.filename)
        
        # Agregar timestamp para evitar conflictos
        import time
        import uuid
        
        # Generar un nombre de archivo único
        unique_id = str(uuid.uuid4().hex[:16])
        timestamp = str(int(time.time()))
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}_{unique_id}{ext}"
        
        file_path = os.path.join(upload_path, filename)
        print(f"Guardando archivo en: {file_path}")
        
        try:
            file.save(file_path)
            print(f"Archivo guardado exitosamente en: {file_path}")
            
            # Verificar que el archivo se haya guardado correctamente
            if not os.path.exists(file_path):
                print("Error: El archivo no se guardó correctamente")
                return jsonify({'error': 'Error al guardar el archivo'}), 500
                
            # Construir la URL de la imagen
            # Usar una ruta relativa al directorio static
            image_url = f"/static/uploads/{filename}"
            print(f"URL de la imagen: {image_url}")
            
            # Verificar que el archivo se pueda acceder a través de la ruta web
            import urllib.request
            try:
                # Verificar que el archivo existe localmente
                if not os.path.exists(file_path):
                    print(f"Error: El archivo no se encuentra en la ruta: {file_path}")
                    return jsonify({'error': 'Error al guardar el archivo'}), 500
                    
                # Verificar que el archivo tenga un tamaño mayor a 0
                if os.path.getsize(file_path) == 0:
                    print(f"Error: El archivo está vacío: {file_path}")
                    return jsonify({'error': 'El archivo está vacío'}), 500
                    
                print(f"Archivo subido exitosamente: {file_path} ({os.path.getsize(file_path)} bytes)")
                return jsonify({'image_url': image_url})
                
            except Exception as e:
                print(f"Error al verificar el archivo: {str(e)}")
                return jsonify({'error': f'Error al verificar el archivo: {str(e)}'}), 500
                
        except Exception as e:
            print(f"Error al guardar el archivo: {str(e)}")
            return jsonify({'error': f'Error al guardar el archivo: {str(e)}'}), 500
    
    return jsonify({'error': 'Tipo de archivo no permitido. Formatos permitidos: png, jpg, jpeg, gif, webp'}), 400
