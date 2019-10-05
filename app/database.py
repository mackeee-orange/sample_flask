from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import force_auto_coercion
from flask_migrate import Migrate
from contextlib import contextmanager

db = SQLAlchemy()


def init_db(_app: Flask) -> None:
    """
    DBの初期化・マイグレーション
    """
    force_auto_coercion()  # パスワードを暗号化してDBに保存するために必要
    db.init_app(_app)
    Migrate(_app, db)


@contextmanager
def session_scope() -> Session:
    session = db.session()
    try:
        yield session
    except SQLAlchemyError:
        session.rollback()
        raise
