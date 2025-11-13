"""
HTTP module for Flo
Provides HTTP server and client functionality
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from typing import Dict, Callable, Any
import re


class FloHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Flo applications"""
    
    routes: Dict[str, Dict[str, Callable]] = {}
    
    def do_GET(self):
        self.handle_request('GET')
    
    def do_POST(self):
        self.handle_request('POST')
    
    def do_PUT(self):
        self.handle_request('PUT')
    
    def do_DELETE(self):
        self.handle_request('DELETE')
    
    def handle_request(self, method: str):
        # Parse path and find matching route
        for pattern, handlers in self.routes.items():
            match = re.match(pattern, self.path)
            if match and method in handlers:
                handler = handlers[method]
                params = match.groupdict()
                
                try:
                    # Call the handler
                    result = handler(**params)
                    
                    # Handle response
                    if isinstance(result, dict):
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps(result).encode())
                    elif isinstance(result, str):
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(result.encode())
                    elif isinstance(result, int):
                        # HTTP status code
                        self.send_response(result)
                        self.end_headers()
                    else:
                        self.send_response(200)
                        self.send_header('Content-Type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(str(result).encode())
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': str(e)}).encode())
                return
        
        # No route found
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Custom logging
        print(f"[HTTP] {format % args}")


class FloApp:
    """Flo HTTP application"""
    
    def __init__(self):
        self.routes = {}
    
    def route(self, path: str, method: str = 'GET'):
        """Decorator to register a route"""
        def decorator(func):
            # Convert Flo-style path params to regex
            pattern = path
            pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
            pattern = f'^{pattern}$'
            
            if pattern not in self.routes:
                self.routes[pattern] = {}
            
            self.routes[pattern][method.upper()] = func
            return func
        
        return decorator
    
    def listen(self, port: int):
        """Start the HTTP server"""
        FloHTTPHandler.routes = self.routes
        
        server = HTTPServer(('0.0.0.0', port), FloHTTPHandler)
        print(f"Flo server listening on port {port}")
        
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped")
            server.shutdown()


# Module exports
app = FloApp()


def get(path: str):
    """Decorator for GET routes"""
    return app.route(path, 'GET')


def post(path: str):
    """Decorator for POST routes"""
    return app.route(path, 'POST')


def put(path: str):
    """Decorator for PUT routes"""
    return app.route(path, 'PUT')


def delete(path: str):
    """Decorator for DELETE routes"""
    return app.route(path, 'DELETE')
