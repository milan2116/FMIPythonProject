"""
Application setup and configuration.

This module initializes the core components and services of the Flask application,
including the app instance, database, migration tool, user authentication, email service, 
and password hashing.

Components initialized:
    - Flask app instance: `app`
    - SQLAlchemy for database management: `db`
    - Flask-Migrate for database migrations: `migrate`
    - Flask-Login for user authentication: `login_manager`
    - Flask-Mail for sending emails: `mail`
    - Argon2 password hashing: `ph`

Configuration is loaded from the `config.Config` class, which contains necessary
settings like the database URI and secret keys.

Additionally, the `login_manager` is configured with a login view set to `'login'`,
which determines where users will be redirected if they are not authenticated.

Imports:
    - `routes` and `models`: Modules where the routes and database models for the app are defined.

This module essentially sets up all the essential Flask extensions needed for the application 
to function properly and manage user sessions, database interactions, and email communication.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from argon2 import PasswordHasher

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)
ph = PasswordHasher()

login_manager.login_view = 'login'

from app import routes, models