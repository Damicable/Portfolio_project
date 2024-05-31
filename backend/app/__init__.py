from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from flask_cors import CORS # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# load environment variables from the .env file
load_dotenv()

# secret_key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
# db configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt_manager = JWTManager(app)

app.url_map.strict_slashes = False

with app.app_context():
    from app.models import *
    from app.routes import *
    from app.controllers import *
    
    db.create_all() # type: ignore
