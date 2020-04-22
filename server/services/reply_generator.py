import requests
from generator import generator
import logging
log = logging.getLogger('app.create_app')


def perform(entry, access_token):
    return ReplyGenerator(entry, access_token).run()


class ReplyGenerator:
    def __init__(self, entry, access_token):
        self.entry = entry
        self.access_token = access_token

    def run(self):
        user_message = self.entry['messaging'][0]['message']['text']
        user_id = self.entry['messaging'][0]['sender']['id']

        messages = self.handle_message(user_id, user_message)
        log.info(f'received messages: {messages}')

        if messages is None:
            return

        for message in messages:
            yield {
                'messaging_type': 'RESPONSE',
                'recipient': {'id': user_id},
                'message': {'text': message["text"]}
            }

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
        log.info(f'received profile {profile}')
        first_person = " ".join([profile["first_name"], profile["last_name"]])

        return generator.perform(
            session=None,
            first_person=first_person,
            second_person=self.second_person(first_person),
            text=user_message,
            truncate=True,
            length=200
        )

    def second_person(self, first_person):
        if first_person == "Luke Olney":
            return "Ted Olney-Bell"
        return "Luke Olney"
