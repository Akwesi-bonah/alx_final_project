#!/usr/bin/python3
""" Define Student class """
from werkzeug.security import generate_password_hash

from models.base_model import BaseModel, Base
import models
from sqlalchemy import Column, String, Date


class Student(BaseModel, Base):
    """Represent student in hostel"""

    if models.storage_t == "db":
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
        password = Column(String(1000))
        disability = Column(String(128))
    else:
        full_name = ""
        date_of_birth = ""
        gender = ""
        student_number = ""
        program = ""
        level = ""
        email = ""
        address = ""
        phone = ""
        guardian_name = ""
        guardian_phone = ""
        password = ""
        disability = ""

    def __init__(self, *args, **kwargs):
        """initialization of Student class"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = generate_password_hash(value)
        super().__setattr__(name, value)

    def __str__(self):
        """returns a string representation of the object"""
        return self.first_name + " " + self.last_name

    @property
    def get_id(self):
        """returns the id of the object"""
        return str(self.id)


