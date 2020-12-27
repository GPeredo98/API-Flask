import os

# JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
JWT_SECRET_KEY = 'super_secret'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost:3306/api_flask'
CORS_HEADERS = 'Content-Type'
