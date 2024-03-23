#!/usr/bin/python3
"""Define Booking class"""


import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey,Numeric


class Booking(BaseModel, Base):
    """Represent booking in hostel"""

    __tablename__ = "bookings"
    room_id = Column(String(60), ForeignKey('rooms.id',
                                                ondelete="CASCADE"), nullable=False)
    student_id = Column(String(60), ForeignKey('students.id',
                                                   ondelete="CASCADE"), nullable=False)
    paid = Column(Numeric(8,2), default=0)
    status = Column(String(128), default="pending")



    def __init__(self, *args, **kwargs):
        """Initialize booking class"""
        super().__init__(*args, **kwargs)

