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
    hashed_password = Column(String(250), nullable=False)
    role = Column(String(128))
    status = Column(String(10))
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, *args, **kwargs):
        """initialization of Staff class"""
        super().__init__(*args, **kwargs)
        self._hashed_password = None

    # @property
    # def password(self) -> str:
    #     """ Getter of the password
    #     """
    #     return self._hashed_password
    #
    # @password.setter
    # def password(self, value):
    #     """ Setter of the password
    #     """
    #     salt = bcrypt.gensalt()
    #     self._hashed_password = bcrypt.hashpw(value.encode(), salt)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(value.encode(), salt)
        super().__setattr__(name, value)

    def display_name(self) -> str:
        """ Display Username based on email/first_name/last_name
        """
        return f"{self.name} { self.last_name} "

    def is_valid_password(self, pwd):
        """
        validate user password
        :param pwd: password to check
        :return: true of false
        """
        if pwd is None or type(pwd) is not str:
            return False
        if self.password is None:
            return False
        # Encode both the provided password and the stored hashed password
        stored_password = self.password.encode()
        pwd_encoded = pwd.encode()
        return bcrypt.checkpw(pwd_encoded, stored_password)







