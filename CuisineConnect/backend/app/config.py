from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config:
    """Config for application"""
    
    username = getenv('DB_USERNAME')
    password = getenv('DB_PASSWORD')
    host = getenv('DB_HOST')
    db_name = getenv('DB_NAME')
    
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{username}:{password}@{host}/{db_name}'
    SECRET_KEY = getenv('SECRET_KEY')

config = Config()
