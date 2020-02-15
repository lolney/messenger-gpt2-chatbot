from services import reply_generator
import requests


def perform(*args):
    return ReplySender(*args).run()


class ReplySender():
    def __init__(self, data, access_token):
        self.data = data
        self.access_token = access_token

    def run(self):
        for entry in self.data["entry"]:
            user_id = entry['messaging'][0]['sender']['id']

            self.typing(user_id)
            messages = reply_generator.perform(entry, self.access_token)

            for message in messages:
                response = requests.post(
                    'https://graph.facebook.com/v6.0/me/messages',
                    params=self.params(),
                    json=message
                )

                if not response.ok:
                    raise Exception(response.json())

            self.typing(user_id, on=False)

    def typing(self, user_id, on=True):
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
