import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class BaseConfig:
    # For SQLite, we don't need DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT
    DB_NAME = os.getenv('DB_NAME', 'app.db')  # Default to 'app.db' if not provided
    DB_NAME_TEST = os.getenv('DB_NAME_TEST', 'test_app.db')  # Default test database name

    # SQLite connection format
    CONN = f'sqlite:///{os.path.join(basedir, DB_NAME)}'
    
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    APP_PORT = os.getenv('APP_PORT')
    APP_HOST = os.getenv('APP_HOST')
    APP_ENV = os.getenv('APP_ENV')
    APP_PREFIX = '/api'

    TOKEN_EXPIRED = 60 * 24 * 5


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 4
    # Use SQLite database for development
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, BaseConfig.DB_NAME)}'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    # Use a separate SQLite database for testing
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, BaseConfig.DB_NAME_TEST)}'
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    # Use SQLite database for production
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{os.path.join(basedir, BaseConfig.DB_NAME)}'
