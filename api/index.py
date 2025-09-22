import os
import sys
import json
import logging
from io import BytesIO
from urllib.parse import parse_qs

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Asegurarse de que el directorio raíz esté en el path
root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, root_path)
logger.info(f"Python path: {sys.path}")

# Importar la aplicación Flask después de configurar el path
try:
    from main import app as application
    logger.info("Aplicación Flask importada correctamente")
except ImportError as e:
    logger.error(f"Error al importar la aplicación Flask: {e}")
    raise

def lambda_handler(event, context):
    """Manejador principal para las solicitudes de API Gateway"""
    try:
        # Obtener información de la solicitud
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '')
        headers = {k.lower(): v for k, v in event.get('headers', {}).items()}
        query_params = event.get('queryStringParameters', {}) or {}
        body = event.get('body', '')
        
        logger.info(f"Procesando solicitud: {method} {path}")
        logger.debug(f"Headers: {headers}")
        logger.debug(f"Query params: {query_params}")
        
        # Procesar el cuerpo de la solicitud
        content_type = headers.get('content-type', '').lower()
        if content_type == 'application/json' and body:
            try:
                if isinstance(body, str):
                    body = json.loads(body)
                logger.debug(f"Cuerpo JSON: {json.dumps(body, indent=2)}")
            except json.JSONDecodeError as e:
                logger.warning(f"Error al decodificar JSON: {e}")
                body = {}
        
        # Crear entorno WSGI
        environ = {
            'REQUEST_METHOD': method,
            'PATH_INFO': path,
            'QUERY_STRING': '&'.join([f"{k}={v}" for k, v in query_params.items()]),
            'CONTENT_TYPE': content_type,
            'CONTENT_LENGTH': str(len(str(body)) if body else 0),
            'SERVER_NAME': headers.get('host', 'localhost'),
            'SERVER_PORT': headers.get('x-forwarded-port', '80'),
            'SERVER_PROTOCOL': 'HTTP/1.1',
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': headers.get('x-forwarded-proto', 'http'),
            'wsgi.input': BytesIO(json.dumps(body).encode('utf-8') if body and not isinstance(body, str) else str(body or '').encode('utf-8')),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'HTTP_COOKIE': headers.get('cookie', ''),
        }
        
        # Agregar cabeceras HTTP al entorno
        for key, value in headers.items():
            environ[f'HTTP_{key.upper().replace("-", "_")}'] = value
        
        # Variables para capturar la respuesta
        response_headers = []
        response_body = []
        
        def start_response(status, headers, exc_info=None):
            nonlocal response_headers
            response_headers = [status] + headers
            return response_body.append
        
        # Procesar la solicitud con la aplicación Flask
        try:
            result = application(environ, start_response)
            
            # Recopilar la respuesta
            try:
                for data in result:
                    if data:
                        response_body.append(data.decode('utf-8') if isinstance(data, bytes) else str(data))
            finally:
                if hasattr(result, 'close'):
                    result.close()
            
            # Procesar la respuesta
            if not response_headers:
                response_headers = ['200 OK', ('Content-Type', 'text/plain')]
            
            status_line = response_headers[0] if response_headers else '200 OK'
            status_code = int(status_line.split(' ')[0]) if status_line else 200
            
            # Convertir encabezados a diccionario
            headers_dict = {}
            for header in response_headers[1:]:
                if len(header) >= 2:
                    key, value = header[0], header[1]
                    headers_dict[key] = value
            
            # Asegurar Content-Type
            if 'Content-Type' not in headers_dict:
                headers_dict['Content-Type'] = 'application/json'
            
            # Construir respuesta
            response = {
                'statusCode': status_code,
                'headers': headers_dict,
                'body': ''.join(response_body) if response_body else ''
            }
            
            logger.info(f"Respuesta exitosa: {status_code}")
            return response
            
        except Exception as e:
            logger.error(f"Error al procesar la solicitud: {str(e)}", exc_info=True)
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'error': 'Error al procesar la solicitud',
                    'message': str(e),
                    'type': type(e).__name__
                })
            }
            
    except Exception as e:
        logger.error(f"Error en lambda_handler: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'error': 'Error interno del servidor',
                'message': str(e),
                'type': type(e).__name__
            })
        }

# Función de entrada para Vercel
def handler(event, context):
    return lambda_handler(event, context)
