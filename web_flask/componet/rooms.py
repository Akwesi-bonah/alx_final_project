#!/usr/bin/env python3
"""  room management"""

from models.room import Room
from models.block import Block
from models.room_type import RoomType
from sqlalchemy.orm import aliased
from web_flask.componet import staff_view
from flask import Blueprint, render_template, request, redirect, url_for
from web_flask.forms.rooms import RoomForm
from models import storage


@staff_view.route('/room', methods=['GET'], strict_slashes=False)
def rooms():
    """Display all rooms"""
    form = RoomForm()
    RoomAlias = aliased(Room)
    BlockAlias = aliased(Block)
    RoomTypeAlias = aliased(RoomType)

    all_rooms = storage.session.query(
        Room.id,
        Room.room_name.label('name'),
        Room.gender,
        Room.floor,
        Room.no_of_beds,
        Block.name.label('block_name'),
        RoomType.name.label('room_type_name')
    ).join(Block, Room.block_id == Block.id
           ).join(RoomType, Room.room_type_id == RoomType.id).all()

    rooms = []
    for result_tuple in all_rooms:
        id, room_name, gender, floor, no_of_beds, block_name, room_type_name = result_tuple

        result_dict = {
            'id': id,
            'name': room_name,
            'gender': gender,
            'floor': floor,
            'no_of_beds': no_of_beds,
            'block_name': block_name,
            'room_type_name': room_type_name
        }
        rooms.append(result_dict)
    return render_template('rooms.html',
                           rooms=rooms, form=form)
