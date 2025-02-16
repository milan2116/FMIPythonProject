"""
Configuration class for setting up application settings.

This class contains various configuration options for the Flask application,
including secret keys, database URI, email settings, and other important variables.
The values can be set using environment variables, with fallback default values
for local development.

Attributes:
    SECRET_KEY (str): Secret key for securing sessions and other sensitive data.
    SQLALCHEMY_DATABASE_URI (str): URI for connecting to the application's database.
    SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables Flask-SQLAlchemy modification tracking.
    MAIL_SERVER (str): The mail server to be used for sending emails.
    MAIL_PORT (int): The port to connect to the mail server.
    MAIL_USE_TLS (bool): Enables TLS encryption for email communication.
    MAIL_USERNAME (str): The username for the email account used to send emails.
    MAIL_PASSWORD (str): The password for the email account.

The values of `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `MAIL_USERNAME`, and `MAIL_PASSWORD`
are read from environment variables. If the environment variables are not set, default values 
are used for local development (such as a default `SECRET_KEY` and `SQLITE` database).
"""
import os

class Config:
    """
    Configuration class for setting up application settings.

    This class contains various configuration options for the Flask application,
    including secret keys, database URI, email settings, and other important variables.
    The values can be set using environment variables, with fallback default values
    for local development.

    Attributes:
        SECRET_KEY (str): Secret key for securing sessions and other sensitive data.
        SQLALCHEMY_DATABASE_URI (str): URI for connecting to the application's database.
        SQLALCHEMY_TRACK_MODIFICATIONS (bool): Disables Flask-SQLAlchemy modification tracking.
        MAIL_SERVER (str): The mail server to be used for sending emails.
        MAIL_PORT (int): The port to connect to the mail server.
        MAIL_USE_TLS (bool): Enables TLS encryption for email communication.
        MAIL_USERNAME (str): The username for the email account used to send emails.
        MAIL_PASSWORD (str): The password for the email account.

    The values of `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `MAIL_USERNAME`, and `MAIL_PASSWORD`
    are read from environment variables. If the environment variables are not set, default values 
    are used for local development (such as a default `SECRET_KEY` and `SQLITE` database).
    """
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///flashcards.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
