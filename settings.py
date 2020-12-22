import os

SECRET_KEY = os.environ.get('SECRET_KEY')

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/api_flask'
CORS_HEADERS = 'Content-Type'
