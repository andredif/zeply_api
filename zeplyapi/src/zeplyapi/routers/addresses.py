import json
import os
import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Path, Depends
from sqlalchemy.orm import Session

from ..exceptions import *
from ..models import models
from ..schemas import *
from ..utils import get_or_create_data
from ..dependencies import get_api_key,get_db, BTC_hd_wallet, ETH_hd_wallet
from ..crud import *


DEFAULT_RESPONSE = {
    404: {
        "description": "Not found"
    },
    500: {
        "description": "Internal Error"
    }
}

router = APIRouter(
    prefix="/addresses",
    tags=["addresses"],
    responses=DEFAULT_RESPONSE,
    dependencies=[Depends(get_api_key)]
)


@router.post("/generate-address", response_model=AddressResponse)
def generate_addresses(
    data: AddressRequest = Body(..., description="data for address generation"),
    db: Session = Depends(get_db)
):
    coin_type = data.coin
    if coin_type == Coin.BTC:
        wallet = BTC_hd_wallet
    elif coin_type == Coin.ETH:
        wallet = ETH_hd_wallet
    saved_addresses = get_all_addresses_from_coin(db=db, coin=coin_type)
    wallet.get_wallet