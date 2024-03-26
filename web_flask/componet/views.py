#!/usr/bin/python3
""" Default staff view"""
import base64

import bcrypt
from sqlalchemy import func,  or_
from werkzeug.security import check_password_hash

from models.block import Block
from models.booking import Booking
from models.payment import Payment
from models.room import Room
from models.room_type import RoomType
from models.staff import Staff
from models.student import Student
from web_flask.componet import staff_view
from flask import render_template,  redirect, url_for, session
import models
from web_flask.forms.login import Login


@staff_view.route('/login', methods=['GET', 'POST'])
def base():
    """Default page - Login"""
    form = Login()
    error_message = None
    user = None
    script = None
    try:
        if form.validate_on_submit():
            session.clear()
            email = form.email.data
            password = form.password.data
            user_data = models.storage.find_by(Staff, email=email)
            data = f'{email}:{password}'
            token = base64.b64encode(data.encode()).decode()  # Encode the data to base64
            script = f"<script>localStorage.setItem('token', '{token}')</script>"  # Correct syntax for setting localStorage
            if user_data is None or bcrypt.checkpw(password.encode(), user_data.password.encode()):
                session['user_id'] = user_data.id
                session['user'] = email
                return redirect(url_for('staff_view.dashboard', user=session['user']))
            else:
                error_message = "Invalid email or password"
    except Exception as e:
        print(e)
        error_message = "An error occurred, please try again"
    return render_template('default.html', form=form, error=error_message, script=script)

@staff_view.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('staff_view.base'))


@staff_view.route('/user', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

        total_beds = models.storage.session.query(
            func.sum(Room.no_of_beds)).scalar()
        total_rooms = models.storage.session.query(
            func.count(Room.id)).scalar()
        female_beds = (
            models.storage.session.query(
                func.sum(Room.no_of_beds))
            .filter(Room.gender == 'female')
            .scalar()
        )
        male_beds = (
            models.storage.session.query(
                func.sum(Room.no_of_beds))
            .filter(Room.gender == 'male')
            .scalar()
        )

        female_rev = (
            models.storage.session.query(
                func.sum(Room.reserved_beds))
            .filter(Room.gender == 'female').scalar()
        )
        male_rev = (
            models.storage.session.query(
                func.sum(Room.reserved_beds))
            .filter(Room.gender == 'male').scalar()
        )

        allotment_revenue = (
            models.storage.session.query(func.sum(RoomType.price))
            .join(Room, Room.room_type_id == RoomType.id)
            .join(Booking, Booking.room_id == Room.id)
            .filter(
                or_(Booking.status == 'pending', Booking.status == 'paid'))
            .scalar()
        )
        allotment_revenue = allotment_revenue if allotment_revenue else 0

        rooms_per_type = (
            models.storage.session.query(
                Room.room_type_id, func.count(Room.id).label('room_count'))
            .group_by(Room.room_type_id)
            .all()
        )

        room_type_revenues = {}
        for room_type_id, room_count in rooms_per_type:
            room_type = models.storage.session.query(RoomType).get(room_type_id)
            if room_type:
                room_type_revenues[room_type.name] = {
                    'room_count': room_count,
                    'revenue': room_count * room_type.price if room_type.price else 0
                }

        latest_bookings = (
            models.storage.session.query(
                Booking.paid,
                Student.student_number,
                func.concat(
                    Student.first_name,
                    ' ',
                    Student.last_name
                ).label('full_name'),
                Block.name,
                Room.room_name,
                RoomType.name,
                RoomType.price,
                Booking.status
            )
            .join(Student, Booking.student_id == Student.id)
            .join(Room, Booking.room_id == Room.id)
            .join(Block, Room.block_id == Block.id)
            .join(RoomType, Room.room_type_id == RoomType.id)
            .order_by(Booking.id.desc())
            .limit(20)
            .all()
        )
        last_10_bookings_list = []
        for booking in latest_bookings:
            (paid, student_number, name, block_name,
             room_no, room_type, price, status) = booking

            result_tuple = {
                'paid': paid,
                'student_number': student_number,
                'student_name': name,
                'block_name': block_name,
                'room_no': room_no,
                'room_type': room_type,
                'price': price,
                'status': status
            }
            last_10_bookings_list.append(result_tuple)

    latest_payments = (
        models.storage.session.query(
            Payment.amount,
            Payment.reference_id,
            Student.student_number,
            func.concat(
                Student.first_name,
                ' ',
                Student.last_name
            ).label('full_name')

        ).all()
    )

    latest_payments_list = []
    for payment in latest_payments:
        (amount, reference_id, student_number, name) = payment

        result_tuple = {
            'amount': amount,
            'reference_id': reference_id,
            'student_number': student_number,
            'student_name': name,

        }
        latest_payments_list.append(result_tuple)

    return render_template('base.html', user=user,
                           total_beds=total_beds, total_rooms=total_rooms,
                           female_beds=female_beds, male_beds=male_beds,
                           room_type_revenues=room_type_revenues,
                           allotment_revenue=allotment_revenue,
                           male_rev=male_rev, female_rev=female_rev,
                           latest_payments_list=latest_payments_list,
                           latest_booking_list=last_10_bookings_list)


@staff_view.route('/allotment')
def allotment():
    if 'user_id' not in session:
        return redirect(url_for('staff_view.base'))
    else:
        user = session['user']

        allotment_tuple = (
            models.storage.session.query(
                Booking.id,
                Booking.paid,
                Student.student_number,
                Student.phone,
                func.concat(
                    Student.first_name,
                    ' ',
                    Student.last_name
                ).label('full_name'),
                Block.name,
                Room.room_name,
                RoomType.name,
                RoomType.price,
                Booking.status
            )
            .join(Student, Booking.student_id == Student.id)
            .join(Room, Booking.room_id == Room.id)
            .join(Block, Room.block_id == Block.id)
            .join(RoomType, Room.room_type_id == RoomType.id)
            .all()
        )

        allotment_list = []
        for allot in allotment_tuple:
            (booking_id, paid, student_number,phone, name, block_name,
             room_no, room_type, price, status) = allot

            result_tuple = {
                'booking_id': booking_id,
                'paid': paid,
                'student_number': student_number,
                'phone': phone,
                'student_name': name,
                'block_name': block_name,
                'room_no': room_no,
                'room_type': room_type,
                'price': price,
                'status': status
            }
            allotment_list.append(result_tuple)
    return render_template('allotment.html',
                           allotment=allotment_list, user=user)

