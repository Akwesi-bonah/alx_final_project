#!/usr/bin/python3
""" This model defines room type class """
import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, Float


class RoomType(BaseModel, Base):
    """ This class defines room type class """
    __tablename__ = 'room_types'
    name = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    price = Column(Float(precision=2), nullable=False)
    status = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
