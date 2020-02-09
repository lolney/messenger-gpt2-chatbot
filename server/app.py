from flask import Flask, request, Response
import requests
import json
from generator import generator
from generator import session
from services import reply_sender, threaded_reply_sender
import os
app = Flask(__name__)

# env_variables
verify_token = os.getenv('VERIFY_TOKEN', None)
access_token = os.getenv('ACCESS_TOKEN', None)

if not verify_token:
    raise Exception("verify_token not set")
if not access_token:
    raise Exception("access_token not set")

# TODO: try making a global session:
# https://stackoverflow.com/questions/56137254/python-flask-app-with-keras-tensorflow-backend-unable-to-load-model-at-run
#sess = session.load()
sess = None


@app.route('/webhook', methods=['GET'])
def webhook_verify():
    if request.args.get('hub.verify_token') == verify_token:
        return request.args.get('hub.challenge')
    return "Wrong verify token"


@app.route('/webhook', methods=['POST'])
def webhook_action():
    data = json.loads(request.data.decode('utf-8'))
    threaded_reply_sender.perform(data, access_token)
    return Response(response="EVENT RECEIVED", status=200)


@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    entry = data["entry"][0]
    response = next(reply_sender.perform(entry, access_token))
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


@app.route('/privacy', methods=['GET'])
def privacy():
    # needed route if you need to make your bot public
    return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."


@app.route('/', methods=['GET'])
def index():
    return "Hello there, I'm a facebook messenger bot."


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
