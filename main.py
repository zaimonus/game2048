import http.server
import json
import re
from uuid import uuid4

import numpy as np

from game2048 import Game2048, Direction

games = dict()


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


class GameHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if m := re.match(r'/([0-9]{30,40})', self.path):
            if (f_u := int(m.group(1))) in games.keys():
                g = games[f_u]
                g_d = g.as_dict()
                g_d['nodes'] = g.nodes
                msg = json.dumps({'game': g_d}, cls=NumpyArrayEncoder)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(msg.encode())
            else:
                self.send_error(404)
        elif re.match(r'/list', self.path):
            msg = json.dumps({'games': list(map(str, games.keys()))})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg.encode())
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path.startswith('/new'):
            u = uuid4()
            g = Game2048(u)
            games[u.int] = g
            msg = json.dumps({'game': g.as_dict()})
            self.send_response(200)
            self.end_headers()
            self.wfile.write(msg.encode())
        else:
            self.send_error(404)

    def do_PUT(self):
        if m := re.match(r'/([0-9]{30,40})\?=(up|down|left|right)', self.path):
            if (f_u := int(m.group(1))) in games.keys():
                g = games[f_u]
                direction = m.group(2)
                match direction:
                    case 'up':
                        g.move(direction=Direction.UP)
                    case 'down':
                        g.move(direction=Direction.DOWN)
                    case 'left':
                        g.move(direction=Direction.LEFT)
                    case 'right':
                        g.move(direction=Direction.RIGHT)
                msg = json.dumps({'game': g.as_dict()})
                self.send_response(200)
                self.end_headers()
                self.wfile.write(msg.encode())
            else:
                self.send_error(404)
        else:
            self.send_error(404)

    def do_DELETE(self):
        if m := re.match(r'/([0-9]{30,40})', self.path):
            if (f_u := int(m.group(1))) in games.keys():
                del games[f_u]
                self.send_response(200)
                self.end_headers()
            else:
                self.send_error(404)
        else:
            self.send_error(404)


server = http.server.ThreadingHTTPServer(server_address=('localhost', 80), RequestHandlerClass=GameHandler)
server.serve_forever()
