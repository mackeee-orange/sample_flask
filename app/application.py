from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from celery import Celery
from ghidorah.config import Config
from ghidorah.database import init_db
from ghidorah.api import *
from sentry_sdk.integrations.flask import FlaskIntegration
import sentry_sdk
import os


def create_celery(_app: Flask) -> Celery:
    """
    Celeryの初期化
    """
    _celery: Celery = Celery(
        _app.import_name,
        backend=_app.config['CELERY_RESULT_BACKEND'],
        broker=_app.config['CELERY_BROKER_URL'],
        include=['ghidorah.tasks']
    )
    _celery.conf.update(_app.config)

    class ContextTask(_celery.Task):
        def __call__(self, *args, **kwargs):
            with _app.app_context():
                return self.run(*args, **kwargs)

    _celery.Task = ContextTask
    return _celery


def create_app() -> Flask:
    """
    Flaskアプリケーションの初期化
    """
    _app: Flask = Flask(__name__)
    CORS(_app)
    # Flaskのconfigが 設定ファイルを読み込む処理
    _app.config.from_object(Config)
    if _app.config.get('ENV', "development") == "production":
        # Sentryの初期化
        sentry_sdk.init(
            dsn="https://2327ececb80148e28cfcc97d77d56147@sentry.io/1525406",
            integrations=[FlaskIntegration()]
        )

    # DBセッションの暗号化のため
    _app.secret_key = os.urandom(24)
    # DB初期化
    init_db(_app)
    return _app


def bind_routing(_app):
    # ルーティング
    auth_beta_prefix = '/auth/beta/'
    api_beta_prefix = '/api/beta/'
    api_admin_prefix = '/api/admin/'

    api: Api = Api(_app)
    api.add_resource(SignUpAPI, auth_beta_prefix + 'sign_up')
    api.add_resource(SignInAPI, auth_beta_prefix + 'sign_in')

    api.add_resource(AdminTraderBotsAPI, api_admin_prefix + 'trader_bots')
    api.add_resource(AdminTraderBotAPI, api_admin_prefix + 'trader_bots/<id>')
    api.add_resource(AdminCryptoExchangesAPI, api_admin_prefix + 'crypto_exchanges')
    api.add_resource(AdminCryptoExchangeAPI, api_admin_prefix + 'crypto_exchanges/<id>')

    api.add_resource(CurrentAccountAPI, api_beta_prefix + 'accounts/me')
    api.add_resource(CurrentAccountEmergencyStopAPI, api_beta_prefix + 'accounts/me/emergency_stop')
    api.add_resource(CurrentAccountEmailAPI, api_beta_prefix + 'accounts/me/email')
    api.add_resource(CurrentAccountPasswordAPI, api_beta_prefix + 'accounts/me/password')
    api.add_resource(NotifyTargetsAPI, api_beta_prefix + 'notify_targets')
    api.add_resource(NotifyTargetAPI, api_beta_prefix + 'notify_targets/<id>')
    api.add_resource(NotifySettingAPI, api_beta_prefix + 'notify_setting')
    api.add_resource(CryptoExchangesAPI, api_beta_prefix + 'crypto_exchanges')
    api.add_resource(ExchangeApiSettingsAPI, api_beta_prefix + 'exchange_api_settings')
    api.add_resource(ExchangeApiSettingAPI, api_beta_prefix + 'exchange_api_settings/<id>')
    api.add_resource(TraderBotsAPI, api_beta_prefix + 'trader_bots')
    api.add_resource(TraderBotAPI, api_beta_prefix + 'trader_bots/<id>')
    api.add_resource(TradingSettingAPI, api_beta_prefix + 'trading_settings/<id>')
    api.add_resource(MinionsAPI, *[api_beta_prefix + 'minions',
                                   api_beta_prefix + 'minions/report'])
    api.add_resource(MinionAPI, api_beta_prefix + 'minions/<id>')
    api.add_resource(MinionEmergencyStopAPI, api_beta_prefix + 'minions/<id>/emergency_stop')
    api.add_resource(DashBoardAPI, api_beta_prefix + 'dashboard')
    api.add_resource(TimelineAPI, api_beta_prefix + 'timeline')
    api.add_resource(OrdersAPI, api_beta_prefix + 'minions/<minion_id>/orders')
    # api.add_resource(WinRatioApi, )


# For external
app: Flask = create_app()
celery: Celery = create_celery(app)
bind_routing(app)
