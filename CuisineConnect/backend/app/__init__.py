from flask import Flask
from app.db import db
from app.config import Config


def create_app():
    """
    Creates app to run flask.
    """
    app = Flask(__name__)
    
    app.config.from_object(Config)
    
    with app.app_context():
        db.init_app(app)
    
    return app
