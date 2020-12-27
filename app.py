from flask import Flask
from flask_cors import CORS
from utilities import db, ma, jwt
from productos.views import productos
from usuarios.views import usuarios


def create_app(config_file='settings.py'):
    application = Flask(__name__)
    application.config.from_pyfile(config_file)
    CORS(application)
    ma.init_app(application)
    jwt.init_app(application)
    db.init_app(application)
    with application.app_context():
        db.create_all()
    application.register_blueprint(productos, url_prefix='/producto')
    application.register_blueprint(usuarios, url_prefix='/usuario')
    return application


if __name__ == '__main__':
    app = create_app()
    app.run(debug=False, port=4000)
