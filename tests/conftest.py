import pytest
import os


from app import create_app
from extensions import db
from src.models.user_model import User
from src.models.account_model import Account
from src.models.transaction_model import Transaction


@pytest.fixture()
def app():
    os.environ['FLASK_ENV'] = 'testing'
    app = create_app()

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()
