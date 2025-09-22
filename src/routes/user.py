from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash

user_bp = Blueprint('user', __name__)

# Credenciales de administrador (en producción, usa una base de datos)
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'  # En producción, usa una contraseña segura y guárdala en variables de entorno

@user_bp.route('/test')
def test():
    return {'message': 'User routes working'}

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Verificar credenciales (en producción, usa una base de datos)
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return jsonify({'success': True, 'message': 'Inicio de sesión exitoso'})
    else:
        return jsonify({'success': False, 'message': 'Credenciales incorrectas'}), 401

@user_bp.route('/check-auth', methods=['GET'])
def check_auth():
    return jsonify({'authenticated': session.get('admin_logged_in', False)})

@user_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('admin_logged_in', None)
    return jsonify({'success': True, 'message': 'Sesión cerrada correctamente'})
