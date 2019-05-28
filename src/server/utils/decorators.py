from functools import wraps

import os
from flask import Flask

from server.extensions import db


def flask_db_connector():
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kw):
            app = Flask(__name__)
            app_settings = os.getenv(
                'APP_SETTINGS', 'server.config.GettingDataForModelsConfig')
            app.config.from_object(app_settings)
            db.init_app(app)
            with app.app_context():
                return func(*args, **kw)
        return wrapper
    return decorator
