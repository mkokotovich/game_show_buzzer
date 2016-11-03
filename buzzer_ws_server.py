
import argparse
import random
import os

import cherrypy

from ws4py.server.cherrypyserver import WebSocketPlugin, WebSocketTool
from ws4py.websocket import WebSocket
from ws4py.messaging import TextMessage
from ws4py.client.threadedclient import WebSocketClient

gteams = []

class BuzzerSocketHandler(WebSocket):
    def received_message(self, m):
        global gteams
        team = str(m)
        if team not in gteams:
            cherrypy.log("Team added : %s" % team)
            gteams.append(team)
        msg = "<h1>Teams have buzzed:</h1>"
        msg += "<br>".join("Team: " + t for t in gteams)
        cherrypy.engine.publish('websocket-broadcast', msg)

class BuzzerServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.scheme = 'ws'

    @cherrypy.expose
    def index(self):
        return """<html>
    <head>
      <script type='application/javascript' src='https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js'></script>
      <script type='application/javascript'>
        $(document).ready(function() {
          websocket = '%(scheme)s://%(host)s:%(port)s/ws';
          if (window.WebSocket) {
            ws = new WebSocket(websocket);
          }
          else if (window.MozWebSocket) {
            ws = MozWebSocket(websocket);
          }
          else {
            console.log('WebSocket Not Supported');
            return;
          }
          ws.onmessage = function (evt) {
             document.getElementById('output').innerHTML = evt.data;
          };
          $('#buzz').click(function() {
             console.log($('#teamname').val());
             ws.send($('#teamname').val());
             return false;
          });
        });
      </script>
    </head>
    <body>
        <a href="/reset">Reset buzzer</a>
    <form action='#' id='chatform' method='get'>
      <label id='output'><h1>Ready to buzz!</h1></textarea>
      <br />
      <label for='message'>Team name: </label><input type='text' id='teamname' />
      <input id='buzz' type='submit' value='Buzz!' />
      </form>
    </body>
    </html>
    """ % {'host': self.host, 'port': self.port, 'scheme': self.scheme}

    @cherrypy.expose
    def ws(self):
        cherrypy.log("Handler created: %s" % repr(cherrypy.request.ws_handler))

    @cherrypy.expose
    def reset(self):
        global gteams
        gteams = []
        raise cherrypy.HTTPRedirect("/")

if __name__ == '__main__':
    import logging
    from ws4py import configure_logger
    configure_logger(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Game Show Buzzer')
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-p', '--port', default=9000, type=int)
    args = parser.parse_args()

    cherrypy.config.update({'server.socket_host': args.host,
                            'server.socket_port': args.port,
                            'tools.staticdir.root': os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))})

    WebSocketPlugin(cherrypy.engine).subscribe()
    cherrypy.tools.websocket = WebSocketTool()

    cherrypy.quickstart(BuzzerServer(args.host, args.port), '', config={
        '/ws': {
            'tools.websocket.on': True,
            'tools.websocket.handler_cls': BuzzerSocketHandler
            },
        '/js': {
              'tools.staticdir.on': True,
              'tools.staticdir.dir': 'js'
            }
        }
    )
