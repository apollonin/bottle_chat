from bottle import request, Bottle, abort, template, static_file
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

from pymongo import MongoClient

import json
import gevent


from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

app = Bottle()

db = MongoClient('mongodb', 27017)

class SocketIOApp(object):
    """Stream sine values"""
    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/socket.io'):
            socketio_manage(environ, {'': ChatNamespace});

class ChatNamespace(BaseNamespace):
    _registry = {}

    def initialize(self):
        self._registry[id(self)] = self

    def disconnect(self, *args, **kwargs):
        del self._registry[id(self)]
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    def on_login(self, message):
        pass

    def on_chat(self, message):
        db.bottle.messages.insert_one(json.loads(message));
        self._broadcast('chat', message)
        

    def _broadcast(self, event, message):
        for s in self._registry.values():
            s.emit(event, message)

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/app')

@app.route('/')
def index():
    return template('index')


@app.route('/history')
def getHistory():

    cursor = db.bottle.messages.find()

    messages = []

    for message in cursor:
        messages.append({'name': message['name'], 'message': message['message']})

    return {'messages' : messages}



# setup server to handle webserver requests
http_server = WSGIServer(('0.0.0.0', 8080), app, handler_class=WebSocketHandler)

# setup server to handle websocket requests
sio_server = SocketIOServer(
    ('0.0.0.0', 9999), SocketIOApp(),
    namespace="socket.io",
    policy_server=False
)

gevent.joinall([
    gevent.spawn(http_server.serve_forever),
    gevent.spawn(sio_server.serve_forever)
])