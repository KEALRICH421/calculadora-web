"""
Módulo que contiene el servidor web para la calculadora.
"""
import http.server
import socketserver
import urllib.parse
import json
import os
from calculadora.operaciones import Calculadora

class ManejadorCalculadora(http.server.SimpleHTTPRequestHandler):
    """Manejador de solicitudes HTTP para la calculadora."""
    
    def do_GET(self):
        """Maneja solicitudes GET."""
        if self.path == '/':
            # Servir la página principal
            self.servir_pagina_principal()
        elif self.path.startswith('/static/'):
            # Servir archivos estáticos
            self.servir_archivo_estatico()
        else:
            # Ruta no encontrada
            self.enviar_error(404, "Página no encontrada")
    
    def do_POST(self):
        """Maneja solicitudes POST para operaciones de calculadora."""
        if self.path == '/calcular':
            self.procesar_calculo()
        else:
            self.enviar_error(404, "Ruta no encontrada")
    
    def servir_pagina_principal(self):
        """Sirve la página HTML principal."""
        try:
            with open('templates/index.html', 'rb') as f:
                contenido = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(contenido)
        except FileNotFoundError:
            self.enviar_error(500, "Error interno del servidor")
    
    def servir_archivo_estatico(self):
        """Sirve archivos estáticos (CSS, JS, etc.)."""
        try:
            ruta_archivo = self.path[1:]  # Remover el '/' inicial
            
            # Mapeo de extensiones a tipos MIME
            tipos_mime = {
                '.css': 'text/css',
                '.js': 'application/javascript',
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.ico': 'image/x-icon'
            }
            
            extension = os.path.splitext(ruta_archivo)[1].lower()
            tipo_contenido = tipos_mime.get(extension, 'application/octet-stream')
            
            with open(ruta_archivo, 'rb') as f:
                contenido = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', tipo_contenido)
            self.end_headers()
            self.wfile.write(contenido)
        except FileNotFoundError:
            self.enviar_error(404, "Archivo no encontrado")
        except Exception as e:
            self.enviar_error(500, f"Error interno del servidor: {str(e)}")
    
    def procesar_calculo(self):
        """Procesa una operación de calculadora."""
        try:
            # Obtener y parsear los datos del formulario
            longitud = int(self.headers['Content-Length'])
            datos = self.rfile.read(longitud).decode('utf-8')
            parametros = urllib.parse.parse_qs(datos)
            
            # Extraer parámetros
            operacion = parametros.get('operacion', [''])[0]
            numero1 = parametros.get('numero1', [''])[0]
            numero2 = parametros.get('numero2', [''])[0]
            expresion = parametros.get('expresion', [''])[0]
            
            # Realizar la operación correspondiente
            resultado = self.ejecutar_operacion(operacion, numero1, numero2, expresion)
            
            # Enviar respuesta JSON
            respuesta = {
                'estado': 'exito',
                'resultado': resultado,
                'operacion': operacion
            }
            
            self.enviar_respuesta_json(200, respuesta)
            
        except Exception as e:
            # Enviar error
            respuesta = {
                'estado': 'error',
                'mensaje': str(e)
            }
            self.enviar_respuesta_json(400, respuesta)
    
   
    def ejecutar_operacion(self, operacion, numero1, numero2, expresion):
        """Ejecuta la operación matemática solicitada."""
        if operacion == 'expresion':
            return Calculadora.evaluar_expresion(expresion)
        elif operacion == 'raiz':
            return Calculadora.raiz_cuadrada(numero1)
        elif operacion == 'porcentaje':
            return Calculadora.porcentaje(numero1, numero2)
        elif operacion == 'potencia':
            return Calculadora.potencia(numero1, numero2)
        else:
            # Operaciones binarias básicas
            operaciones = {
                'suma': Calculadora.suma,
                'resta': Calculadora.resta,
                'multiplicacion': Calculadora.multiplicacion,
                'division': Calculadora.division
            }

            if operacion in operaciones:
                return operaciones[operacion](numero1, numero2)
            else:
                raise ValueError("Operación no válida")
    
    def enviar_respuesta_json(self, codigo, datos):
        """Envía una respuesta JSON."""
        contenido = json.dumps(datos).encode('utf-8')
        
        self.send_response(codigo)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)
    
    def enviar_error(self, codigo, mensaje):
        """Envía una página de error."""
        pagina_error = f"""
        <html>
        <head><title>Error {codigo}</title></head>
        <body>
            <h1>Error {codigo}</h1>
            <p>{mensaje}</p>
            <a href="/">Volver a la calculadora</a>
        </body>
        </html>
        """
        
        contenido = pagina_error.encode('utf-8')
        
        self.send_response(codigo)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(contenido)))
        self.end_headers()
        self.wfile.write(contenido)

def iniciar_servidor(puerto=8000, host=''):
    """Inicia el servidor web de la calculadora."""
    with socketserver.TCPServer((host, puerto), ManejadorCalculadora) as httpd:
        print(f"Servidor de calculadora ejecutándose en http://{host or 'localhost'}:{puerto}")
        print("Presiona Ctrl+C para detener el servidor")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido")
