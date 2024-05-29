from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# load environment variables from the .env file
load_dotenv()

# secret_key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# db configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

with app.app_context():
    from app.models import *
    from app.routes import *
    from app.controllers import *
    
    db.create_all()
