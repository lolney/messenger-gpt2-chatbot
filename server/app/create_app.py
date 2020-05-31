from flask import Flask, request, Response
from requests_futures.sessions import FuturesSession
from urllib.parse import urljoin
import json
import logging
import requests
from services import reply_sender, reply_generator, webhook_proxy

log = logging.getLogger('app.create_app')

default_env = {
    'VERIFY_TOKEN': None,
    'ACCESS_TOKEN': None,
    'URL': 'localhost:8080'
}


def create_app(env=default_env):
    app = Flask(__name__)
    # TODO: try making a global session:
    # https://stackoverflow.com/questions/56137254/python-flask-app-with-keras-tensorflow-backend-unable-to-load-model-at-run
    #sess = session.load()

    @app.route('/webhook', methods=['GET'])
    def webhook_verify():
        if request.args.get('hub.verify_token') == env["VERIFY_TOKEN"]:
            return request.args.get('hub.challenge')
        return "Wrong verify token"

    @app.route('/webhook', methods=['POST'])
    def webhook_action():
        # step 1
        url = urljoin(env["URL"], 'send_reply_proxy')
        log.info(f"webhook called with {request.data}")
        FuturesSession().post(url, data=request.data)
        return Response(status=200)

    @app.route('/generate', methods=['POST'])
    def generate():
        # call to generate directly, bypassing webhook process
        data = json.loads(request.data.decode('utf-8'))
        entry = data["entry"][0]
        response = list(reply_generator.perform(entry, env["ACCESS_TOKEN"]))
        return Response(
            response=json.dumps(response),
            status=200,
            mimetype='application/json'
        )

    @app.route('/send_reply_proxy', methods=['POST'])
    def send_reply_proxy():
        # step 2
        webhook_proxy.perform(request.data)
        return Response(
            status=200
        )

    @app.route('/send_reply', methods=['POST'])
    def send_reply():
        # step 4
        data = json.loads(request.data.decode('utf-8'))
        reply_sender.perform(data, env["ACCESS_TOKEN"])
        return Response(response="REPLY SENT", status=200)

    @app.route('/privacy', methods=['GET'])
    def privacy():
        # needed route if you need to make your bot public
        return "This facebook messenger bot's only purpose is to [...]. That's all. We don't use it in any other way."

    @app.route('/', methods=['GET'])
    def index():
        return "Hello there, I'm a facebook messenger bot."

    return app
