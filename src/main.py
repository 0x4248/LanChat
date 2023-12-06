# LanChat
# Chat with friends on your local lan
# GitHub: https://www.github.com/lewisevans2007/LanChat
# Licence: GNU General Public Licence v3.0
# By: Lewis Evans

import flask
from flask import request, jsonify, Response
import os
import json

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route("/chat")
def chat():
    return flask.render_template('chat.html')

@app.route('/send', methods=['GET'])
def send():
    name = request.args.get('name')
    message = request.args.get('message')
    if "<script>" in name or "<script>" in message:
        return Response(status=400)
    elif name == "" or message == "":
        return Response(status=400)
    if os.path.exists('messages.json'):
        with open('messages.json', 'r') as f:
            data = json.load(f)
            data['messages'].append({'name': name, 'message': message})
        with open('messages.json', 'w') as f:
            json.dump(data, f)
    else:
        with open('messages.json', 'w') as f:
            data = {'messages': [{'name': name, 'message': message}]}
            json.dump(data, f)
    return Response(status=200)

@app.route('/messages', methods=['GET'])
def messages():
    if os.path.exists('messages.json'):
        with open('messages.json', 'r') as f:
            data = json.load(f)
            return jsonify(data)
    else:
        return Response(status=204)

@app.route('/clear', methods=['GET'])
def clear():
    if os.path.exists('messages.json'):
        os.remove('messages.json')
    return Response(status=200)

@app.route('/status', methods=['GET'])
def status():
    if os.path.exists('messages.json'):
        return Response(status=200)
    else:
        return Response(status=204)

@app.route('/fetch_ip', methods=['GET'])
def fetch_ip():
    return request.remote_addr

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)