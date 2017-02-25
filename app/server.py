from bottle import request, Bottle, abort, template
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

from pymongo import MongoClient

import json
from bson import ObjectId

from bson.json_util import dumps


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# TODO. rework this to singleton
class MongoConnection(object):
    
    __metaclass__ = Singleton

    def getConnection(self):
        client = MongoClient('mongodb', 27017)
        return client

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

app = Bottle()

@app.route('/websocket')
def handle_websocket():
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            if (message == 'getHistory'):
                wsock.send(dumps({
                        'type': 'history',
                        'data': getHistory()
                    }))
            else:
                wsock.send(dumps({
                        'type': 'message',
                        'data': message
                    }))

                #save to DB
                message = json.loads(message)
                client = MongoConnection().getConnection()
                client.bottle.messages.insert_one(message).inserted_id

        except WebSocketError:
            break

@app.route('/history')
def getHistory():

    client = MongoConnection().getConnection()

    cursor = client.bottle.messages.find()

    messages = []

    for message in cursor:
        messages.append(JSONEncoder().encode(message))

    return messages

server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()