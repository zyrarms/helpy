from socket import socket
from sanitybot import create_app
from flask import request, jsonify
from chat import chat
from utils import pdd_prediction

app = create_app()
# app.config['SECRET_KEY'] = 'secret'
# socketio = SocketIO(app)

# # chatbot prediction model
@app.post("/predict")
def predict():
    text1 = request.get_json().get("message")
    # TODO: check if text is valid
    response = chat(text1)
    print(response)
    message = {"answer": response}
    return jsonify(message)

@app.post("/predict_epds")
def predict_epds():
    text1 = request.get_json().get("message")
    # TODO: check if text is valid
    response = pdd_prediction(text1)
    print(response)
    message = {"answer": response}
    return jsonify(message)

# @socketio.on('message')
# def handleMessage(msg):
#     text1 = request.get_json().get("message")
#     # TODO: check if text is valid
#     response = chat(text1)
#     message = {"answer": response}
#     send(message, broadcast=True )
#     return jsonify(message)
    


if __name__ == '__main__':
    app.run(debug=True)