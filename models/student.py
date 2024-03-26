#!/usr/bin/python3
""" Define Student class """
import bcrypt
from werkzeug.security import generate_password_hash

from models.base import BaseModel, Base
import models
from sqlalchemy import Column, String, Date


class Student(BaseModel, Base):
    """Represent student in hostel"""

    __tablename__ = "students"
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    other_name = Column(String(128))
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String(128), nullable=False)
    student_number = Column(String(128), unique=True)
    program = Column(String(128))
    level = Column(String(128))
    email = Column(String(128), unique=True)
    address = Column(String(128))
    phone = Column(String(128), unique=True)
    guardian_name = Column(String(128))
    guardian_phone = Column(String(128))
    disability = Column(String(128))
    profile_picture = Column(String(128))
    password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __init__(self, *args, **kwargs):
        """initialization of Student class"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            salt = bcrypt.gensalt()
            value = bcrypt.hashpw(value.encode(), salt)
        super().__setattr__(name, value)

    def __str__(self):
        """returns a string representation of the object"""
        return self.first_name + " " + self.last_name

    def display_name(self) -> str:
        """ Display Username based on email/first_name/other_name/last_name """
        if self.other_name is not None:
            return f"{self.first_name} {self.other_name} {self.last_name}"
        else:
            return f"{self.first_name} {self.last_name}"

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



