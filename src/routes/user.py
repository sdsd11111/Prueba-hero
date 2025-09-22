from flask import Blueprint, request, jsonify, session, current_app
from functools import wraps
import logging

# Configurar logging
logger = logging.getLogger(__name__)

user_bp = Blueprint('user', __name__)

# Credenciales de administrador (en producción, usa una base de datos)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # En producción, usa una contraseña segura y guárdala en variables de entorno

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return jsonify({'error': 'No autorizado'}), 401
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/test')
def test():
    logger.info("Ruta de prueba accedida")
    return jsonify({'message': 'User routes working'})

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        if not request.is_json:
            logger.error("Solicitud sin formato JSON")
            return jsonify({'success': False, 'message': 'Content-Type debe ser application/json'}), 400
            
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        logger.info(f"Intento de inicio de sesión para el usuario: {username}")
        
        if not username or not password:
            logger.warning("Faltan credenciales")
            return jsonify({'success': False, 'message': 'Se requieren nombre de usuario y contraseña'}), 400
        
        # Verificar credenciales (en producción, usa una base de datos)
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session.permanent = True  # Hacer que la sesión sea permanente
            session['admin_logged_in'] = True
            logger.info("Inicio de sesión exitoso")
            return jsonify({
                'success': True, 
                'message': 'Inicio de sesión exitoso',
                'user': {'username': username}
            })
        else:
            logger.warning(f"Credenciales incorrectas para el usuario: {username}")
            return jsonify({
                'success': False, 
                'message': 'Credenciales incorrectas'
            }), 401
            
    except Exception as e:
        logger.error(f"Error en el inicio de sesión: {str(e)}", exc_info=True)
        return jsonify({
            'success': False, 
            'message': 'Error interno del servidor',
            'error': str(e)
        }), 500

@user_bp.route('/check-auth', methods=['GET'])
def check_auth():
    try:
        is_authenticated = session.get('admin_logged_in', False)
        logger.info(f"Verificación de autenticación: {is_authenticated}")
        return jsonify({
            'authenticated': is_authenticated,
            'user': {'username': ADMIN_USERNAME} if is_authenticated else None
        })
    except Exception as e:
        logger.error(f"Error al verificar autenticación: {str(e)}", exc_info=True)
        return jsonify({
            'authenticated': False,
            'error': 'Error al verificar la autenticación'
        }), 500

@user_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    try:
        session.pop('admin_logged_in', None)
        logger.info("Sesión cerrada correctamente")
        return jsonify({
            'success': True, 
            'message': 'Sesión cerrada correctamente'
        })
    except Exception as e:
        logger.error(f"Error al cerrar sesión: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': 'Error al cerrar la sesión',
            'error': str(e)
        }), 500
