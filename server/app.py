from flask import Flask, request, Response
import requests
import json
from generator import generator
from generator import session
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
    for entry in data['entry']:
        user_message = entry['messaging'][0]['message']['text']
        user_id = entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = handle_message(user_id, user_message)
        requests.post(
            'https://graph.facebook.com/v2.6/me/messages/?access_token=' + access_token, json=response)
    return Response(response="EVENT RECEIVED", status=200)


@app.route('/webhook_dev', methods=['POST'])
def webhook_dev():
    # custom route for local development
    data = json.loads(request.data.decode('utf-8'))
    user_message = data['entry'][0]['messaging'][0]['message']['text']
    user_id = data['entry'][0]['messaging'][0]['sender']['id']
    response = {
        'recipient': {'id': user_id},
        'message': {'text': handle_message(user_id, user_message)}
    }
    return Response(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


def request_profile(user_id):
    params = {'fields': 'first_name,last_name', 'access_token': access_token}
    response = requests.get(
        f'https://graph.facebook.com/v6.0/{user_id}', params=params)
    if not response.ok:
        raise Exception(response)
    return response.json()


def handle_message(user_id, user_message):
    profile = request_profile(user_id)
    print('Received profile', profile)
    first_person = " ".join([profile["first_name"], profile["last_name"]])

    return generator.perform(
        session=sess,
        first_person=first_person,
        second_person="Peter Olney",
        text=user_message,
        truncate=True,
        length=50
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
