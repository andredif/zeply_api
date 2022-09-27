import enum
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String, Integer, Enum, DateTime, Text, Float
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from ..database.database import Base
from ..schemas import Coin


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    coin = Column(Enum(Coin))
    address = Column(String)



