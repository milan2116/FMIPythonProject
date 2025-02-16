import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from app import app, db
from app.models import User, Deck, Flashcard

@pytest.fixture
def client():
    """
    Creates a test client and an in-memory SQLite database.
    Sets up and tears down the database for each test.
    """
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
