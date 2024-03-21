#!/usr/bin/python3
from sqlalchemy import text, func, and_

import models
from models import storage
from models.block import Block
from models.booking import Booking
from models.configuration import Configuration
from models.room import Room
from models.room_type import RoomType

from models.staff import Staff

from models.student import Student

config = storage.session.query(
            Configuration.created_by,
            Configuration.created_at,
            Configuration.expiry_date
        ).all()
print(config)