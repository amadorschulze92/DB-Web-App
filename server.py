"""Template Induction Tool

Usage:
  server.py [DEFAULT_DOCUMENT_DIRECTORY]
  server.py (-h | --help)
  server.py --version
"""
import os
import logging

from werkzeug import cached_property
from werkzeug.wrappers import Request
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.serving import run_simple


STATIC_DIR = os.path.join(os.path.dirname(__file__), 'statics')


class App(object):
    def __call__(self, environ, start_response):
        urls = self.url_map.bind_to_environ(environ)
        endpoint, args = urls.match()
        response = endpoint(Request(environ), **args)
        return response(environ, start_response)

    @cached_property
    def url_map(self):
        from urls import url_map
        return url_map


def make_app():
    from werkzeug.debug import DebuggedApplication

    app = SharedDataMiddleware(App(), {'/statics': STATIC_DIR})
    app = DebuggedApplication(app, evalex=True)
    return app


if __name__ == "__main__":
    app = make_app()
    from web_service import run_wsgi_app_with_cherrypy
    run_wsgi_app_with_cherrypy(app)
else:
    app = make_app()
