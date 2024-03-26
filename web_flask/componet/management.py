#!/usr/bin/env python3
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
    """Display all blocks.

    This function is responsible for rendering the 'manageBlock.html' template
    and displaying all blocks. It first checks if the 'user_id' is present in
    the session. If not, it redirects to the 'base' route of the 'staff_view'
    blueprint. Otherwise, it retrieves the user from the session.

    The function also initializes an 'AddBlock' form and retrieves all blocks
    from the storage. It then converts each block to a dictionary and stores
    them in the 'blocks' list.

    Finally, it renders the 'manageBlock.html' template, passing the 'blocks',
    'form', and 'user' variables as template arguments.

    Returns:
        The rendered template 'manageBlock.html' with the 'blocks', 'form', and
        'user' variables passed as template arguments.
    """
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

    form = AddBlock()
    all_blocks = storage.all(Block).values()
    blocks = [block.to_dict() for block in all_blocks]

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
