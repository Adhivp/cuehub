from pyramid.config import Configurator
from pyramid.response import Response

def hello_world(request):
    return Response('Hello, Pyramid!')

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('home', '/')
        config.add_view(hello_world, route_name='home')
        app = config.make_wsgi_app()

    from waitress import serve
    serve(app, host='0.0.0.0', port=6543)
