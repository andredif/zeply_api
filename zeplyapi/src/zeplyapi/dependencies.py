import logging
from fastapi import Security
from fastapi.security.api_key import APIKeyHeader

from .models import models
from .database.database import SessionLocal, engine
from . import config as env
from . import exceptions as custom_exception
from .wallet.hd_wallet import HdWalletHandler
from .schemas import Coin


models.Base.metadata.create_all(bind=engine)

API_KEY = env.settings.ZEPLY_API_KEY
api_key_header = APIKeyHeader(name=env.settings.API_KEY_NAME, auto_error=False)
BTC_hd_wallet = HdWalletHandler(Coin.BTC)
ETH_hd_wallet = HdWalletHandler(Coin.ETH)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise custom_exception.ForbiddenException()


class CustomLogger(object):

    log_level = {
            "CRITICAL" : 50,
            "ERROR" : 40,
            "WARNING" : 30,
            "INFO" : 20,
            "DEBUG" : 10
        }

    def __init__(self):
        self.logger = logging.getLogger("uvicorn_app")

    def log(
        self, event: str, msg: str, level: str="INFO"
    ):
        return self.logger.log(
            self.log_level.get(level, 20),
            f"{event} - {msg}"
            )