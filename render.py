import os
from os import path
from simplejson import dumps as json_dumps

from werkzeug import Response

from jinja2 import Environment, FileSystemLoader

TEMPLATE_PATH = path.join(path.dirname(__file__), 'templates')
DEFAULT_DIR = os.getcwd()
jinja_env = Environment(autoescape=True,
                        loader=FileSystemLoader(TEMPLATE_PATH),
                        line_statement_prefix='##')


def repr_jinja_filter(s):
    return repr(s)

jinja_env.filters['repr'] = repr_jinja_filter
jinja_env.globals['zip'] = zip
jinja_env.globals['any'] = any
jinja_env.globals['to_json'] = json_dumps


def render_template(template, **context):
    return Response(render(template, **context),
                    mimetype='text/html')


def render(template, **context):
    return jinja_env.get_template(template).render(**context),


def home(_request):
    return render_template('home.html', current_dir=DEFAULT_DIR)


def favicon(_request):
    return Response(status=404)


def boom(_request):
    raise Exception('And BOOM goes the dynamite!')
