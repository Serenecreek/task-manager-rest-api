import pytest

from app import create_app
from app.extensions import db


@pytest.fixture
def app():

    class TestConfig:
        TESTING = True

        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

        SQLALCHEMY_TRACK_MODIFICATIONS = False

        JWT_SECRET_KEY = "test-jwt-secret"

    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_token(client):

    client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/api/auth/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    return response.get_json()["access_token"]