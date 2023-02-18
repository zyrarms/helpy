from socket import socket
from sanitybot import create_app
from flask import request, jsonify, send_file
# from chat import chat
from chat import get_response
from utils import pdd_prediction

app = create_app()
# app.config['SECRET_KEY'] = 'secret'
# socketio = SocketIO(app)

# # chatbot prediction model


@app.post("/predict")
def predict():
    text1 = request.get_json().get("message")
    response = get_response(text1)
    print(response)
    message = {"answer": response}
    return jsonify(message)


@app.post("/predict_epds")
def predict_epds():
    text1 = request.get_json().get("message")
    response = pdd_prediction(text1)
    print(response)
    message = {"answer": response}
    return jsonify(message)


@app.route('/file/<path:filename>')
def serve_file(filename):
    return send_file(filename, as_attachment=True)

# @socketio.on('message')
# def handleMessage(msg):
#     text1 = request.get_json().get("message")
#     response = chat(text1)
#     message = {"answer": response}
#     send(message, broadcast=True )
#     return jsonify(message)


if __name__ == '__main__':
    app.run(debug=True)
