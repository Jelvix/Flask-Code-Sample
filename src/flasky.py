from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


def create_shell_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app_settings = os.getenv('server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    db = SQLAlchemy(app)
    db.init_app(app)
    return app


app = create_shell_app()
