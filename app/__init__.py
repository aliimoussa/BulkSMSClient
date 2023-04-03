from flask import Flask
from api.route import api_bp


def create_app(config_name='Config'):
    app = Flask(__name__)
    app.register_blueprint(api_bp, url_prefix='/api')
    return app


if __name__ == '__main__':
    create_app().run()
