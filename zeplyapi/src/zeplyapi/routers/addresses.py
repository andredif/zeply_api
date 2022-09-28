import json
import os
import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Body, Path, Depends
from sqlalchemy.orm import Session

from .. import exceptions as custom_exception
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
    wallet.generate_new_address(id=len(saved_addresses)+1)
    addresses = wallet.addresses_list()
    new_address = addresses[-1]
    address_data = AddressResponse(
        id=len(saved_addresses)+1,
        coin=coin_type,
        address=new_address
    )
    return create_address(db=db,address_data=address_data)


@router.get("list-addresses", response_model=AddressList)
def list_addresses(
    db: Session = Depends(get_db)
):
    btc_addresses = get_all_addresses_from_coin(db=db, coin=Coin.BTC)
    eth_addresses = get_all_addresses_from_coin(db=db, coin=Coin.ETH)
    return AddressList(
        BTC_addresses=btc_addresses,
        ETH_addresses=eth_addresses
    )


@router.get("retrieve-address/{coin_type}/{address_id}", response_model=AddressResponse)
def retrieve_address(
    coin_type: Coin = Path(..., description="Type of address to be retrieved"),
    address_id: int = Path(..., description="ID of the desired address"),
    db: Session = Depends(get_db)
):
    address = get_address(db=db, coin=coin_type, id=address_id)
    if not address:
        raise custom_exception.NotFoundException("address")
    else:
        return address