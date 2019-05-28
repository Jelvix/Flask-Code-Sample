import os

basedir = os.path.abspath(os.path.dirname(__file__))

db_host = os.getenv('DATABASE_URL', 'db')
db_port = os.getenv('DATABASE_PORT', '5432')
db_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
db_user = os.getenv('DATABASE_USER', 'postgres')
db_name = os.getenv('DATABASE_NAME', 'postgres')


class BaseConfig(object):
    """Base configuration."""
    SECRET_KEY = 'my_precious'
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = 200
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    DEFAULT_EMAIL_DOMAIN = "@gmail.com"


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    BCRYPT_LOG_ROUNDS = 4

    DB_URL = "postgresql+psycopg2://{user}:{password}@{db_host}/{db_name}".format(user=db_user, password=db_password,
                                                                                  db_host=db_host, db_name=db_name)

    SQLALCHEMY_DATABASE_URI = DB_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    WTF_CSRF_ENABLED = False
    DEBUG_TB_ENABLED = True
    OAUTHLIB_INSECURE_TRANSPORT = "2"
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    JWT_ACCESS_TOKEN_EXPIRES = 24*60*60
    OAUTH1_PROVIDER_ENFORCE_SSL = False
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


class TestingConfig(BaseConfig):
    """Testing configuration."""
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    DEBUG_TB_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


