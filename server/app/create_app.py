from flask import Flask, request, Response
import json
from services import reply_sender, threaded_reply_sender

default_env = {
    'VERIFY_TOKEN': None,
    'ACCESS_TOKEN': None
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
        data = json.loads(request.data.decode('utf-8'))
        threaded_reply_sender.perform(data, env["ACCESS_TOKEN"])
        return Response(response="EVENT RECEIVED", status=200)

    @app.route('/webhook_dev', methods=['POST'])
    def webhook_dev():
        # custom route for local development
        data = json.loads(request.data.decode('utf-8'))
        entry = data["entry"][0]
        response = reply_sender.perform(entry, env["ACCESS_TOKEN"])
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

    return app
