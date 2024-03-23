#!/usr/bin/python3
""" Define Rooms class """
import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer


class Room(BaseModel, Base):
    """ Represent room in hostel """
    __tablename__ = "rooms"
    block_id = Column(String(255), ForeignKey('blocks.id',
                                                  ondelete="CASCADE"), nullable=False)
    room_type_id = Column(String(255), ForeignKey('room_types.id',
                                                      ondelete="CASCADE"), nullable=False)
    room_name = Column(String(128), nullable=False, unique=True)
    gender = Column(String(128), nullable=False)
    floor = Column(String(128))
    no_of_beds = Column(Integer, nullable=False)
    booked_beds = Column(Integer)
    reserved_beds = Column(Integer, default=0)
    status = Column(String(128),  default="Available")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

