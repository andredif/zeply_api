from typing import Dict, List, Optional, Tuple
from uuid import UUID

from sqlalchemy.orm import Session

from .schemas import Coin

from .models.models import Address


def create_address(db: Session, address_data):
    db_address = Address(**address_data.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    db.close()
    return db_address


def get_address(db: Session, coin: Coin, id:int):
    db_address = db.query(Address).filter(Address.coin==coin, Address.id==id).first()
    db.close()
    return db_address   


def get_all_addresses_from_coin(db: Session, coin: Coin):
    db_addresses = db.query(Address).filter(Address.coin==coin).all()
    db.close()
    return db_addresses


# def update_address(db: Session, address_id, **kwargs):
#     db_address = db.query(Address).get(address_id)
#     for attribute, value in kwargs.items():
#         setattr(db_address, attribute, value)
#     db.commit()
#     db.refresh(db_address)
#     db.close()
#     return db_address