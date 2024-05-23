from os import getenv


class Config:
    SQLALCHEMY_DATABASE_URI = getenv('DB_URL')
