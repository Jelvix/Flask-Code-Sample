from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_sqlalchemy import SQLAlchemy


from flask_migrate import Migrate

bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
jwt = JWTManager()


def init_api(current_app):
    api = swagger.docs(Api(current_app), apiVersion='0.1', basePath='http://localhost/')
    return api
