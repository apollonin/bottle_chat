from bottle import request, Bottle, abort, template
from gevent.pywsgi import WSGIServer
from geventwebsocket import WebSocketError
from geventwebsocket.handler import WebSocketHandler

from bottle.ext.mongo import MongoPlugin

import json

from bson.json_util import dumps

app = Bottle()

plugin = MongoPlugin(uri="mongodb://mongodb:27017", db="bottle", json_mongo=True)
app.install(plugin)

@app.route('/')
def index():
    return template('blank')


@app.route('/websocket')
def handle_websocket(mongodb):
    wsock = request.environ.get('wsgi.websocket')
    if not wsock:
        abort(400, 'Expected WebSocket request.')

    while True:
        try:
            message = wsock.receive()
            if (message == 'getHistory'):
                wsock.send(dumps({
                        'type': 'history',
                        'data': getHistory(mongodb)
                    }))
            else:
                wsock.send(dumps({
                        'type': 'message',
                        'data': message
                    }))

                #save to DB
                message = json.loads(message)
                mongodb['messages'].insert(message)

        except WebSocketError:
            break

@app.route('/history')
def getHistory(mongodb):

    cursor = mongodb['messages'].find()

    messages = []

    for message in cursor:
        messages.append({'name': message['name'], 'message': message['message']})

    return {'messages' : messages}

server = WSGIServer(("0.0.0.0", 8080), app,
                    handler_class=WebSocketHandler)
server.serve_forever()