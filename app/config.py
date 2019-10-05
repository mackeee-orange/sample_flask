import os
from os.path import join, dirname
from dotenv import load_dotenv
from celery.schedules import crontab

ENV_PATH = join(dirname(__file__), ".env")
load_dotenv(ENV_PATH)


class CommonConfig(object):
    TESTING = False
    SCHEDULER_API_ENABLED = True

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.urandom(24)

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'postgresql://{user}:{password}@{host}:{port}/{db_name}'.format(**{
        "user": os.environ.get("POSTGRES_USER") or "postgres",
        "password": os.environ.get("POSTGRES_PASSWORD") or "postgres",
        "host": os.environ.get("POSTGRES_HOST") or "localhost",
        "port": 5432,
        "db_name": os.environ.get("POSTGRES_NAME") or "ghidorah_development",
    })

    # Celery
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL") or "redis://localhost:6379",
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND") or "redis://localhost:6379"
    INSTALLED_APPS = ['ghidorah']
    CELERYBEAT_SCHEDULE = {
        'run-minion-every-minute': {
            'task': 'ghidorah.lib.schedules.run_orderable_minions.perform',
            'schedule': crontab(minute='*')
        },
        'run-fetch-balance-every-hour': {
            'task': 'ghidorah.lib.schedules.fetch_balance.perform',
            'schedule': crontab(hour='*', minute=0)
        },
        'run-update-order-every-minute': {
            'task': 'ghidorah.lib.schedules.update_opened_orders.perform',
            'schedule': crontab(minute='*')
        }
    }

    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    # MAIL
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT"))
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", True)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")


class DevelopmentConfig(CommonConfig):
    # Flask
    DEBUG = True


class TestingConfig(CommonConfig):
    # Flask
    DEBUG = True


class ProductionConfig(CommonConfig):
    # Flask
    DEBUG = False


_config = {"development": DevelopmentConfig,
           "test": TestingConfig,
           "production": ProductionConfig
           }

Config = _config.get(os.environ.get("FLASK_ENV", "development"))
APP_ROUTE = os.path.dirname(os.path.abspath(__file__))
TMP_LOB_TICK_DIR = os.path.normpath(os.path.join(APP_ROUTE, 'tmp/lob_tick_images'))
