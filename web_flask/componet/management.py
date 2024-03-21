#!/usr/bin/python3
""" Block and Room management"""
from models.room import Room
from models.staff import Staff
from web_flask.componet import staff_view
from flask import Blueprint, render_template, request, redirect, url_for, session
from models.room_type import RoomType
from models.block import Block
from web_flask.forms.block import AddBlock
from web_flask.forms.configuration import ConfigForm
from web_flask.forms.room_type import AddRoomType
from models import storage
from models.configuration import Configuration


@staff_view.route('/block')
def BlockManage():
    """ display all blocks """
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

    form = AddBlock()
    all_bocks = storage.all(Block).values()
    blocks = [block.to_dict() for block in all_bocks]

    return render_template('manageBlock.html',
                           blocks=blocks, form=form, user=user)


@staff_view.route('/roomtype', methods=['GET'], strict_slashes=False)
def room_type():
    form = AddRoomType()
    """ display all room types """

    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']
        all_types = storage.all(RoomType).values()
        types = [room_type.to_dict()
                 for room_type in all_types]

    return render_template('roomType.html',
                           room_type=types,
                           form=form, user=user)


@staff_view.route('/configure')
def configure():
    """ display configuration """
    form = ConfigForm()
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

        config = storage.session.query(
            Staff.name,
            Configuration.created_at,
            Configuration.expiry_date
        ).join(Staff, Configuration.created_by == Staff.id).all()
    
    return render_template('configure.html',
                           form=form, user=user, configure=config)





