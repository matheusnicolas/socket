from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, disconnect
from flask_cors import CORS
import time, json

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = "secret!"
socketio = SocketIO(app)
clients = []

@app.route("/socket")
def socket():
    return render_template("index.html")

# @socketio.on("connected")
# def connected():

def ack():
    return "message was received!"

@socketio.on("device_data")
def handle_message(data):

    while(True):
        time.sleep(5)
        print(data)
        emit("device_response", data, callback=ack, broadcast=True)

def append_client_on_server(sid):
    if (request.sid not in clients):
        clients.append(sid)

def remove_client_on_server(sid):
    if(sid in clients):
        clients.remove(sid)

@socketio.on("device_json_data")
def handle_json(data):
    client_sid = request.sid
    append_client_on_server(client_sid)
    while(True):
        if(client_sid in clients):
            time.sleep(5)
            data = [{}]
            emit("json_response", data, callback=ack(), broadcast=True)

@socketio.on('disconnect')
def test_disconnect():
    print("Entrou 2")
    client_sid = request.sid
    remove_client_on_server(client_sid)
    print('Client disconnected')
    
@socketio.on("error_event")
def on_my_event(data):
    raise RuntimeError()

@socketio.on_error_default
def default_error_handler(e):
    print(request.event["message"])
    print(request.event["args"])

if __name__ == "__main__":
    socketio.run(app, host = "0.0.0.0",port=5000)
