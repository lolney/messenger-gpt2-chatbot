import pytest
import requests


class MockResponse:
    @property
    def ok(self):
        return True

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"first_name": "Luke", "last_name": "Olney"}


class TestWebhook(object):
    @pytest.mark.slow
    def test_generate(self, client, webhook_params, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)
        response = client.post('/generate', data=webhook_params)
        assert response.status_code == 200

    def test_webhook(self, client, webhook_params, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)

        response = client.post('/webhook', data=webhook_params)
        assert response.status_code == 200

    def test_send_reply_proxy(self, client, webhook_params, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)
        monkeypatch.setattr(requests, "post", mock_get)

        response = client.post('/send_reply_proxy', data=webhook_params)
        assert response.status_code == 200

    @pytest.mark.slow
    def test_send_reply(self, client, webhook_params, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)
        monkeypatch.setattr(requests, "post", mock_get)

        response = client.post('/send_reply', data=webhook_params)
        assert response.status_code == 200
