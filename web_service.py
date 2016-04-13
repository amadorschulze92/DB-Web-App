# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import socket
import argparse
import logging

logger = logging.getLogger('milo_logger')

die_message = """
To die: to sleep;
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to"""


def run_wsgi_app_with_cherrypy(app, default_port=8081):
    parser = argparse.ArgumentParser(
        description='Milo Web Service')
    parser.add_argument(
        '--ip', nargs='?', default='localhost',
        help="defaults to %(default)s")
    parser.add_argument(
        '-p', '--port', type=int, default=default_port,
        help="defaults to %(default)s")
    parser.add_argument(
        '-d', '--debug', action='store_true', default=False,
        help="show traceback interpreter on error")
    parser.add_argument(
        '-n', '--threads', type=int, default=30,
        help="number of threads to use")
    parser.add_argument(
        '--port-start', type=int, default=None,
        help="starting port number")
    parser.add_argument(
        '--port-offset', type=int, default=None,
        help="0 based offset to be added to start-port to determine port")

    args = parser.parse_args()

    if args.port_start is not None and args.port_offset is not None:
        port = args.port_start + args.port_offset
    else:
        port = args.port

    if args.debug:
        from werkzeug.debug import DebuggedApplication
        from wsgiref.validate import validator
        app = DebuggedApplication(app, evalex=True)
        app = validator(app)

    from cherrypy import wsgiserver
    import signal
    server = wsgiserver.CherryPyWSGIServer(
        (args.ip, port), app, numthreads=args.threads)

    logger.info('Bringing up server on port %s', port)
    if args.debug:
        from werkzeug.serving import run_with_reloader
        run_with_reloader(server.start)
    else:
        def die_die_die_cherrypy(signum, frame):
            print die_message
            server.stop()
        signal.signal(signal.SIGINT, die_die_die_cherrypy)
        signal.signal(signal.SIGTERM, die_die_die_cherrypy)

        server.start()
