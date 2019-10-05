from app.config import APP_ROUTE, TMP_LOB_TICK_DIR
from app.application import app, celery
import importlib


# View, Modelのロード(PEP8対策)
importlib.import_module("ghidorah.models")
importlib.import_module("ghidorah.api")
importlib.import_module("ghidorah.lib")

