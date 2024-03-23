#!/usr/bin/python3
""" Define Reservation class """
import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String


class Reservation(BaseModel, Base):
    """ Represent reservation in hostel """
    __tablename__ = "reservations"
    room = Column(String(128), nullable=False)
    description = Column(String(128), nullable=False)
    number_of_guests = Column(String(128), nullable=False)
    check_in = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """ initialize reservation class """
        super().__init__(*args, **kwargs)


