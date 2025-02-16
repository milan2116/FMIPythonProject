"""
This module serves as the entry point for running the application.

It imports the `app` object from the `app` module and runs the application 
server in debug mode when executed directly.

Usage:
    To start the application, run this module as the main script:
        python module_name.py

This will launch the app with debugging enabled, allowing for easier 
development and troubleshooting.
"""
from app import app

if __name__ == '__main__':
    app.run(debug=True)
