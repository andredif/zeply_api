import asyncio
import json
import os
import sys
import datetime
import time
from uuid import UUID
import random
from aiohttp import streamer
from sqlalchemy.orm import Session


from .models import *
from .utils import *
from .exceptions import NotFoundException


application_path = os.path.dirname(__file__)

file_dir = os.path.abspath(application_path)
file_path = os.path.join(file_dir, "./data.json")


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        if isinstance(obj, datetime):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def load_data():
    try:
        with open(file_path, "r") as contractFile:
            data = json.load(contractFile)
            contractFile.close()
            return data
    except Exception:
        return load_data()


def save_data(data):
    try:
        with open(file_path, "w") as new_contractFile:
            json.dump(data, new_contractFile, cls=UUIDEncoder)
            new_contractFile.close()
    except Exception:
        return save_data(data)


def get_or_create_data():
    from .dependencies import app_transactor
    from .crud import get_address, create_address
    addresses = app_transactor.wallet.addresses
    db_addresses = []
    for address in addresses:
        get_or_created_address = get_address(address)
        balance = app_transactor.transactor.get_address_balance(address)
        if get_or_created_address is None:
            new_address = AddressInfo(
            address=address,
            balance=balance, 
            )
            get_or_created_address = create_address(new_address)
        get_or_created_address.balance = balance
        db_addresses.append(get_or_created_address)
    return db_addresses