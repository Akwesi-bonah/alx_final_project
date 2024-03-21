#!/usr/bin/python3
"""booking configurations"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, DateTime

from models.staff import Staff


class Configuration(BaseModel, Base):
    if models.storage_t == 'db':
        __tablename__ = "configuration"
        created_by = Column(String(128),
                            ForeignKey(Staff.id,  ondelete="CASCADE"))
        expiry_date = Column(DateTime)
    else:
        created_by = ""
        expiry_date = ""

