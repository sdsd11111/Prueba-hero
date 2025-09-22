from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import json
import os
import sys
from io import BytesIO

# Asegurarse de que el directorio raíz esté en el path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importar la aplicación Flask
from main import app as application

def lambda_handler(event, context):
    # Obtener el método HTTP
    method = event.get('httpMethod', 'GET')
    
    # Obtener la ruta
    path = event.get('path', '')
    
    # Obtener los encabezados
    headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
    
    # Obtener los parámetros de consulta
    query_params = event.get('queryStringParameters', {}) or {}
    
    # Obtener el cuerpo de la solicitud
    body = event.get('body', '')
    if headers.get('content-type', '').startswith('application/json') and body:
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            body = {}
    
    # Crear el entorno WSGI
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_params.items()]),
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body) if isinstance(body, str) else 0),
        'SERVER_NAME': headers.get('host', 'localhost'),
        'SERVER_PORT': headers.get('x-forwarded-port', '80'),
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.version': (1, 0),
        'wsgi.url_scheme': headers.get('x-forwarded-proto', 'http'),
        'wsgi.input': BytesIO(body.encode('utf-8') if isinstance(body, str) else json.dumps(body).encode('utf-8')),
        'wsgi.errors': sys.stderr,
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
    }
    
    # Agregar las cabeceras HTTP al entorno
    for key, value in headers.items():
        key = 'HTTP_' + key.upper().replace('-', '_')
        environ[key] = value
    
    # Variables para capturar la respuesta
    response_headers = []
    response_body = []
    
    def start_response(status, headers, exc_info=None):
        nonlocal response_headers
        response_headers = headers
        return response_body.append
    
    # Procesar la solicitud
    result = application(environ, start_response)
    
    # Recopilar la respuesta
    try:
        for data in result:
            if data:
                response_body.append(data.decode('utf-8') if isinstance(data, bytes) else data)
    finally:
        if hasattr(result, 'close'):
            result.close()
    
    # Convertir la respuesta al formato esperado por Vercel
    status_code = int(response_headers[0].split(' ')[0])
    
    # Convertir las cabeceras a un diccionario
    headers_dict = {}
    for header in response_headers[1:]:
        key, value = header
        headers_dict[key] = value
    
    # Retornar la respuesta
    return {
        'statusCode': status_code,
        'headers': headers_dict,
        'body': ''.join(response_body)
    }

# Esta función es necesaria para Vercel
def handler(event, context):
    return lambda_handler(event, context)
