# api Wsgi con server wsgi
from typing import Any
from webob import Request, Response
from jinja2 import Environment, FileSystemLoader
from parse import parse
from whitenoise import WhiteNoise

class Wsgiclass:
    def __call__(self, environ, start_response):
        #return self.wsgi_app(environ, start_response)
        return self.whitenoise(environ, start_response)
        
    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.solicitud_de_controlador(request)
        return response(environ, start_response)

    def __init__(self, templates_dir="templates", estaticos_dir="estaticos"):
        self.dic_de_rutas = {}
        
        self.templates_env = Environment(
            loader = FileSystemLoader(templates_dir)
        )

        self.whitenoise = WhiteNoise(self.wsgi_app, root=estaticos_dir)
    
    def template(self, template_nombre, context=None):
        if context is None:
            context = {}
        return self.templates_env.get_template(template_nombre).render(**context)

    def ruta(self, path):
        def envoltura(controlador):
            self.dic_de_rutas[path] = controlador
            return controlador
        return envoltura

    def busca_controlador(self, request_path):
        for path, controlador in self.dic_de_rutas.items():
            parseo_resultado = parse(path, request_path)
            if parseo_resultado is not None:
                return controlador, parseo_resultado.named
        return None, None

        
    def solicitud_de_controlador(self, request):
        response = Response()
        controlador, kwargs = self.busca_controlador(request_path=request.path)
        if controlador is not None:
            controlador(request, response, **kwargs)
        else:
            self.respuesta_de_error(response)
        return response

    def respuesta_de_error(self, response):
        response.status_code = 404
        response.text = "Pagina no encontrada"