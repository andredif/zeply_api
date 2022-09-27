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


class Mnemonic(BaseModel):
    word1 : str = Field(example="artic")
    word2 : str = Field(example="artic")
    word3 : str = Field(example="artic")
    word4 : str = Field(example="artic")
    word5 : str = Field(example="artic")
    word6 : str = Field(example="artic")
    word7 : str = Field(example="artic")
    word8 : str = Field(example="artic")
    word9 : str = Field(example="artic")
    word10 : str = Field(example="artic")
    word11 : str = Field(example="artic")
    word12 : str = Field(example="artic")


class AddressRequest(BaseModel):
    coin: Coin

    class Config:
        orm_mode = True


class AddressResponse(BaseModel):
    coin: Coin
    address : str = Field(...,
        example="0xf8b4dFbEEeaffF2E317FFE502d439F174CF7B11a", 
        )

    class Config:
        orm_mode = True


class AddressList(BaseModel):
    addresses : List[str]

