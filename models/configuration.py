#!/usr/bin/python3
"""booking configurations"""

import models
from models.base import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DateTime

from models.staff import Staff


class Configuration(BaseModel, Base):
    __tablename__ = "configuration"
    created_by = Column(String(128),
                            ForeignKey(Staff.id,  ondelete="CASCADE"))
    expiry_date = Column(DateTime)


