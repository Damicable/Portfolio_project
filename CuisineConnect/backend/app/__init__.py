from flask import Flask
from app.db import db
from app.config import Config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

    
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
    
    
def create_app():
    """
    Creates app to run flask.
    """
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        from app.auth.routes import auth_bp
        
        
        app.register_blueprint(auth_bp)
        
        
        db.create_all()
    
    
    return app
