from threading import Thread
from services import reply_sender
import requests


def perform(*args):
    return ThreadedReplySender(*args).start()


class ThreadedReplySender(Thread):
    def __init__(self, data, access_token):
        Thread.__init__(self)
        self.data = data
        self.access_token = access_token

    def run(self):
        for entry in self.data["entry"]:
            user_id = entry['messaging'][0]['sender']['id']

            self.send_typing(user_id)
            messages = reply_sender.perform(entry, self.access_token)
            self.send_typing(user_id, on=False)

            for message in messages:
                response = requests.post(
                    'https://graph.facebook.com/v6.0/me/messages',
                    params=self.params(),
                    json=message
                )

                if not response.ok:
                    raise Exception(response.json())

    def send_typing(self, user_id, on=True):
        url = "https://graph.facebook.com/v6.0/me/messages"
        json = {
            "recipient": {
                "id": user_id
            },
            "sender_action": "typing_on" if on else "typing_off"
        }
        requests.post(url, params=self.params(), json=json)

    def params(self):
        return {
            "access_token": self.access_token
        }
