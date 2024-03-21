#!/usr/bin/python3
""" Define Payment class """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Numeric, ForeignKey


class Payment(BaseModel, Base):
    """Represent payment in hostel"""
    if models.storage_t == "db":
        __tablename__ = "payment"
        booking_id = Column(String(255),
                            ForeignKey('bookings.id',
                                       ondelete="CASCADE"),nullable=False )
        student_id = Column(String(128), ForeignKey('students.id',
                                                    ondelete="CASCADE"), nullable=False)
        reference_id = Column(String(225), nullable=False)
        amount = Column(Numeric(8,2), nullable=False)

    else:
        student_number = ""
        room_name = ""
        amount = 0

    def __init__(self,*args, **kwargs):
        """ initializing payment class """
        super().__init__(*args, **kwargs)

