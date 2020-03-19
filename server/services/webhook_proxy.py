import requests
import os
from urllib.parse import urljoin
import logging
log = logging.getLogger('app.create_app')

url = os.getenv('URL', 'http://localhost:8080')
backoff = 5


def perform(*args):
    return WebhookProxy(*args).run()


class WebhookProxy():
    def __init__(self, data):
        self.data = data

    def run(self):
        for attempt in range(0, backoff):
            log.info(f'Starting attempt {attempt} for data {self.data}')
            response = requests.post(
                urljoin(url, 'send_reply'), data=self.data
            )
            if response.ok:
                break
        log.error(f'Failed {backoff} attempts for data {self.data}')
