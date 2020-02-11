import requests


class MockResponse:
    @property
    def ok(self):
        return True

    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {"first_name": "Luke", "last_name": "olney"}


class TestWebhook(object):
    def test_webhook_dev(self, client, webhook_params, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)
        response = client.post('/webhook_dev', data=webhook_params)
        assert response.status_code == 200

    def test_webhook(self, client, webhook_params, monkeypatch):
        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr(requests, "get", mock_get)
        monkeypatch.setattr(requests, "post", mock_get)

        response = client.post('/webhook', data=webhook_params)
        assert response.status_code == 200