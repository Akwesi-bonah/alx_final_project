#!/usr/bin/python3

from flask import Blueprint, render_template, session, redirect, url_for

from models import storage
from models.block import Block
from models.room import Room
from models.room_type import RoomType
from models.student import Student
from web_flask.componet import staff_view
from web_flask.forms.reserve import ReservationForm


@staff_view.route('/reserve_bed')
def reserve():
    """This function renders the reservation page"""
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

    form = ReservationForm()
    return render_template('reserve.html',
                           form=form, user=user)


@staff_view.route('/assignBed')
@staff_view.route('/assignBed')
def assign_bed():
    """This function renders the assign bed page"""
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    user = session['user']

    reserve_rooms = (
        storage.session.query(
            Room.id, Room.room_name, Room.reserved_beds,
            Block.name, Room.gender,
            RoomType.price, RoomType.name
        )
        .join(Block)
        .join(RoomType)
        .filter(Room.reserved_beds > 0)
        .all()
    )
    rooms_list = []
    for result_tuple in reserve_rooms:
        (room_id, room_name, reserved_beds, block_name, gender,
         price, room_type_name) = result_tuple
        room_dict = {
            'id': room_id,
            'room_name': room_name,
            'reserved_beds': reserved_beds,
            'block_name': block_name,
            'gender': gender,
            'price': price,
            'room_type_name': room_type_name
        }
        rooms_list.append(room_dict)

    students = storage.session.query(
        Student.id, Student.first_name, Student.last_name,
        Student.student_number).all()
    students_list = []
    for result_tuple in students:
        (student_id, first_name, last_name, number) = result_tuple
        student_dict = {
            'id': student_id,
            'first_name': first_name,
            'last_name': last_name,
            'number': number
        }
        students_list.append(student_dict)

    return render_template('assignBed.html', rooms=rooms_list,
                           students=students_list, user=user)


