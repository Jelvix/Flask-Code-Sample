# -*- coding: utf-8 -*-
from flask import Flask, request, redirect

import os

from server.extensions import bcrypt, db, migrate, mail, jwt, init_api
from server.trade_data.exceptions import register_errors
from server.user.google_auth.view import google_blueprint, initialize_black_list_loader
from .api_urls import api_urls


def create_app(script_info=None, settings_name='server.config.DevelopmentConfig'):
    app = Flask(__name__,
                template_folder='../client/templates',
                static_folder='../client/static')

    app_settings = os.getenv(
        'APP_SETTINGS', settings_name)
    app.config.from_object(app_settings)

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    register_errors(app)
    app.config.update({
        'OAUTH1_PROVIDER_ENFORCE_SSL': False
    })

    app.shell_context_processor({'app': app, 'db': db})
    api = init_api(app)
    api_urls(api)
    app.register_blueprint(google_blueprint)

    initialize_black_list_loader()

    return app


if __name__ == '__main__':
    app = create_app()
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '2'
    app.run(host="0.0.0.0", port=9000, debug=True)
