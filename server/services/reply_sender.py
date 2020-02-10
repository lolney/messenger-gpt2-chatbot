import requests
from generator import generator


def perform(*args):
    return ReplySender(*args).run()


class ReplySender:
    def __init__(self, entry, access_token):
        self.entry = entry
        self.access_token = access_token

    def run(self):
        user_message = self.entry['messaging'][0]['message']['text']
        user_id = self.entry['messaging'][0]['sender']['id']
        response = {
            'recipient': {'id': user_id},
            'message': {}
        }
        response['message']['text'] = self.handle_message(
            user_id, user_message)
        return response

    def request_profile(self, user_id):
        params = {'fields': 'first_name,last_name',
                  'access_token': self.access_token}
        response = requests.get(
            f'https://graph.facebook.com/v6.0/{user_id}', params=params)
        if not response.ok:
            raise Exception(response)
        return response.json()

    def handle_message(self, user_id, user_message):
        profile = self.request_profile(user_id)
        print('Received profile', profile)
        first_person = " ".join([profile["first_name"], profile["last_name"]])

        return generator.perform(
            session=None,
            first_person=first_person,
            second_person="Peter Olney",
            text=user_message,
            truncate=True,
            length=100
        )
