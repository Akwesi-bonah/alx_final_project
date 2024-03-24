#!/usr/bin/env python3
""" Define Staff class """
import bcrypt

from models.base import BaseModel, Base
from sqlalchemy import Column, String


class Staff(BaseModel, Base):
    """ Represent staff in hostel """
    __tablename__ = "staff"
    campus = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(255), nullable=True, unique=True)
    password = Column(String(250), nullable=False)
    role = Column(String(128))
    status = Column(String(10))
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, *args, **kwargs):
        """initialization of Staff class"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Sets a password with bcrypt encryption"""
        if name == "password":
            salt = bcrypt.gensalt()
            value = bcrypt.hashpw(value.encode(), salt)
        super().__setattr__(name, value)

    def display_name(self) -> str:
        """ Display Username based on email/first_name/last_name
        """
        return f"{self.name} { self.last_name} "

    def is_valid_password(self, pwd):
        """Checks if the provided password is valid"""
        if pwd is None or not isinstance(pwd, str):
            return False
        if not self.password:
            return False

        return bcrypt.checkpw(pwd.encode(), self.password.encode())









