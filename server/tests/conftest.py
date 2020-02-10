from app import create_app
import pytest
import json


@pytest.yield_fixture(scope='session')
def mock_app():
    """
    Setup our flask test app, this only gets executed once.
    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'SERVER_NAME': 'test'
    }

    _app = create_app.create_app()
    _app.config.update(params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.yield_fixture(scope='function')
def client(mock_app):
    """
    Setup an app client, this gets executed for each test function.
    :param app: Pytest fixture
    :return: Flask app client
    """
    yield mock_app.test_client()


@pytest.yield_fixture
def webhook_params():
    yield json.dumps({
        "entry": [{"messaging": [{"message": {"text": "test"}, "sender": {"id": "10220109418679421"}}]}]
    })
