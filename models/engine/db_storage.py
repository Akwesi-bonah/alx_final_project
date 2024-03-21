#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models.booking import Booking
from models.configuration import Configuration
from models.payment import Payment
from models.room import Room
from models.room_type import RoomType
from models.staff import Staff
from models.student import Student
from models.reservation import Reservation
from models.block import Block

classes = {
    "Block": Block,
    "Booking": Booking,
    "Payment": Payment,
    "Room": Room,
    "RoomType": RoomType,
    "Staff": Staff,
    "Student": Student,
    "Reservation": Reservation,
    "Configuration": Configuration
}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HMS_MYSQL_USER = getenv('HMS_MYSQL_USER')
        HMS_MYSQL_PWD = getenv('HMS_MYSQL_PWD')
        HMS_MYSQL_HOST = getenv('HMS_MYSQL_HOST')
        HMS_MYSQL_DB = getenv('HMS_MYSQL_DB')
        HMS_ENV = getenv('HMS_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HMS_MYSQL_USER,
                                             HMS_MYSQL_PWD,
                                             HMS_MYSQL_HOST,
                                             HMS_MYSQL_DB))
        #if HMS_ENV == "test":
        #Base.metadata.drop_all(self.__engine)

    @property
    def session(self):
        """Return sessions object"""
        return self.__session

    def get_user_id(self, email=None):
        """ get user id using email """
        if email is None:
            return None
        all_users = self.all(Staff)
        for user in all_users.values():
            if user.email == email:
                return user.id
        return None

    def get_user_email(self, email=None):
        """ check if email exist """
        if email is None:
            return None
        all_users = self.all(Staff)
        for user in all_users.values():
            if user.email == email:
                return True
        return False

    def get_user_pwd(self, email=None):
        """ get user id using email """
        if email is None:
            return None
        all_users = self.all(Staff)
        for user in all_users.values():
            if user.email == email:
                return user.password
        return False

    def get_user_phone(self, phone=None):
        """Get user phone using email"""
        phone = (self.__session.query(Staff).
                 filter_by(phone=phone).first())
        if phone:
            return True
        return False

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
