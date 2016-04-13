from werkzeug.routing import Map, Rule
from werkzeug import Response

from endpoints import home


def favicon(_request):
    return Response(status=404)


url_map = Map([
    Rule('/', endpoint=home.home, strict_slashes=False),
    Rule('/home.css', endpoint=home.css),
    Rule('/get_var', endpoint=home.get_var),
    Rule('/run', endpoint=home.run),
    Rule('/blah', endpoint=home.blah),
    Rule('/favicon', endpoint=favicon)
])
