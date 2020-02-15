from threading import Thread
import requests
import os
from urllib.parse import urljoin
import logging
log = logging.getLogger('app.create_app')

url = os.getenv('MY_URL', 'localhost:8080')
backoff = 5


def perform(*args):
    return ThreadedWebhookProxy(*args).start()


class ThreadedWebhookProxy(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

    def run(self):
        for attempt in range(0, backoff):
            log.info(f'Starting attempt {attempt} for data {self.data}')
            response = requests.post(
                urljoin(url, 'generate'), json=self.data
            )
            if response.ok:
                break
        log.error(f'Failed {backoff} attempts for data {self.data}')
