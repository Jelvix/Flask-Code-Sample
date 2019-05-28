import os
from celery import Celery

from flask import Flask
import flask

from server.extensions import db, mail


class FlaskCelery(Celery):
    def __init__(self, *args, **kwargs):

        super(FlaskCelery, self).__init__(*args, **kwargs)
        self.patch_task()

        if 'app' in kwargs:
            self.init_app(kwargs['app'])

    def patch_task(self):
        TaskBase = self.Task
        _celery = self

        class ContextTask(TaskBase):
            abstract = True

            def __call__(self, *args, **kwargs):
                if flask.has_app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                else:
                    with _celery.app.app_context():
                        return TaskBase.__call__(self, *args, **kwargs)

        self.Task = ContextTask

    def init_app(self, app):
        self.app = app
        self.config_from_object(app.config)


def make_celery(app):
    celery = FlaskCelery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                         broker=app.config['CELERY_BROKER_URL'], app=app)
    celery.conf.update(app.config)
    return celery


def get_celery_app_with_db():
    flask_app = Flask(__name__,
                      template_folder='../../client/templates',
                      static_folder='../../client/static')

    app_settings = os.getenv(
        'APP_SETTINGS', 'server.config.CeleryConfig')
    flask_app.config.from_object(app_settings)
    celery = make_celery(flask_app)
    db.init_app(flask_app)
    mail.init_app(flask_app)
    return celery
