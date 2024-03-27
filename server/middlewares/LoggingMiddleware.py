from werkzeug.wrappers import Request, Response
import json, time

# TODO: see if still needed

class LoggingMiddleware:

    def __init__(self, app):
        self.app = app

    def dispatch_request(self, request):
        return Response(request.method, status=200)

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        print(f"Request: {request.method} {request.path}")
        start_time = time.time()
        response = self.app(environ, start_response)
        return response

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)