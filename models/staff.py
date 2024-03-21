#!/usr/bin/python3
""" Define Staff class """
from hashlib import md5
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String


class Staff(BaseModel, Base):
    """ Represent staff in hostel """
    if models.storage_t == "db":
        __tablename__ = "staff"
        campus = Column(String(255),nullable=True)
        name = Column(String(255), nullable=False)
        email = Column(String(255), nullable=False, unique=True)
        phone = Column(String(255), nullable=True, unique=True)
        password = Column(String(1000))
        role = Column(String(128))
        status = Column(String(128),)
    else:
        campus = ""
        name = ""
        email = ""
        phone = ""
        password = ""
        role = ""
        status = ""

    def __init__(self, *args, **kwargs):
        """initialization of Staff class"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = generate_password_hash(value)
        super().__setattr__(name, value)

    def __str__(self):
        """returns a string representation of the object"""
        return self.name

    def get_id(self):
        """returns the id of the object"""
        return self.id


