from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/socket')
def socket():
    return render_template("index.html")

def ack():
    return 'message was received!'

@socketio.on('message')
def handle_message(data):
    while(True):
        time.sleep(5)
        print(data)
        emit('message', data, callback=ack(), broadcast=True)

@socketio.on('jsonn')
def handle_json(json):
    print(json)

@socketio.on("error_event")
def on_my_event(data):
    raise RuntimeError()

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])
    print(request.event["args"])

if __name__ == '__main__':
    socketio.run(app, host = '0.0.0.0',port=5000)