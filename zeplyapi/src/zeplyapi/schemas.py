from asyncio import tasks
import enum
import string
import random
from typing import Any, Dict, List, Optional, Tuple
import uuid
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime

def gen_float():
    return random.uniform(1.2, 5.4)

def gen_addr():
    possible = string.hexdigits
    return '0x' + ''.join(random.choice(possible) for _ in range(40))


class Coin(enum.Enum):
    BTC = "BTC"
    ETH = "ETH"


class AddressRequest(BaseModel):
    coin: Coin

    class Config:
        orm_mode = True


class AddressResponse(BaseModel):
    id: int
    coin: Coin
    address : str = Field(...,
        example="0xf8b4dFbEEeaffF2E317FFE502d439F174CF7B11a", 
        )

    class Config:
        orm_mode = True


class AddressList(BaseModel):
    BTC_addresses : Optional[List[AddressResponse]]
    ETH_addresses : Optional[List[AddressResponse]]

