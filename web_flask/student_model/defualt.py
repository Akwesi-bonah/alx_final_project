import bcrypt
from sqlalchemy import func, and_
from werkzeug.security import check_password_hash

from models.booking import Booking
from models.student import Student
from web_flask.forms.login import Login
from web_flask.forms.password import ChangePasswordForm
from web_flask.forms.student import StudentForm
from web_flask.student_model import student_views
from flask import render_template, session, redirect, url_for, flash, request
from models import storage
from models.room import Room
from models.block import Block
from models.room_type import RoomType

# JIBRIL@1234
@student_views.route('/', methods=['GET', 'POST'])
def default():
    form = StudentForm()
    error_message = None

    try:
        if request.method == 'POST':
            session.clear()

            email = request.form['email']
            password = request.form['password']

            user_data = storage.find_by(Student, email=email)

            if user_data is not None and bcrypt.checkpw(password.encode(), user_data.password.encode()):
                session['user_id'] = user_data.id
                session['user'] = email
                return redirect(url_for('student_views.dashboard'))
            else:
                error_message = "Invalid email or password"
    except Exception as e:
        print(e)
        error_message = "An error occurred, please try again"

    # Pass the error_message to the template
    return render_template('Sdefault.html',
                           form=form,
                           error_message=error_message)


@student_views.route('/logout', methods=['GET'])
def Slogout():
    if 'user_id' in session:
        session.clear()
        return redirect(url_for('student_views.default'))


@student_views.route('/default/student', methods=['GET'])
def dashboard():
    """Student dashboard"""
    if 'user' not in session:
        return redirect(url_for('student_views.default'))
    else:
        block = storage.all(Block).values()
        blocks = [block.to_dict() for block in block]
        room_types = storage.all(RoomType).values()
        room_type = [room_type.to_dict() for room_type in room_types]
        user_id = session['user_id']
        user = storage.get(Student, user_id)
        gender = user.gender

        room = (storage.session.query(Room.id, Room.room_name, Room.booked_beds, Room.floor, Room.gender,
                                      RoomType.name.label('room_type_name'), RoomType.price,
                                      Block.name.label('block_name'))
                .join(Block, Room.block_id == Block.id)
                .join(RoomType, Room.room_type_id == RoomType.id)
                .filter(and_(Room.booked_beds > 0,
                 Room.gender == gender)).all())

        rooms = []
        for result_tuple in room:
            (id, room_name, no_of_beds, floor,
             gender, room_type_name, price,
             block_name) = result_tuple

            result_dict = {
                'id': id,
                'room_name': room_name,
                'no_of_beds': no_of_beds,
                'floor': floor,
                'gender': gender,
                'room_type_name': room_type_name,
                'price': price,
                'block_name': block_name
            }

            rooms.append(result_dict)

    return render_template('Sbase.html',
                           blocks=block,
                           room_types=room_type,
                           rooms=rooms)


@student_views.route('/default/student/profile', methods=['GET'])
def student_profile():
    """Student profile"""
    form = StudentForm()
    reset = ChangePasswordForm()
    user = None
    if 'user_id' not in session:
        return redirect(url_for('student_views.default'))
    else:

        try:
            id = session['user_id']
            user = storage.get(Student, id)
            user = user.to_dict()
            print(user)
            form.first_name.data = user['first_name']
            form.last_name.data = user['last_name']
            form.other_name.data = user['other_name']
            form.email.data = user['email']
            form.phone.data = user['phone']
            form.student_number.data = user['student_number']
            form.program.data = user['program']
            form.level.data = user['level']
            form.guardian_name.data = user['guardian_name']
            form.guardian_phone.data = user['guardian_phone']
            form.disability.data = user['disability']
            form.gender.data = user['gender']
            form.address.data = user['address']
            form.date_of_birth.data = user['date_of_birth']
        except Exception as e :
            pass

    return render_template('Sprofile.html',
                           form=form, user=user, reset=reset)


@student_views.route('/default/student/mybooking', methods=['GET'])
def my_bookings():
    """ Display student booking information """
    if 'user_id' not in session:
        return redirect(url_for('student_views.default'))

    user_id = session['user_id']

    user = storage.session.query(Student).filter(Student.id == user_id).first()

    if not user:
        return redirect(url_for('student_views.default'))

    # Query to fetch booking information for the student
    my_booking = storage.session.query(
        Booking.id,
        Room.room_name.label('room_name'),
        RoomType.name.label('room_type_name'),
        Block.name.label('block_name'),
        Booking.status,
        Booking.paid,
        func.concat(Student.first_name, ' ', Student.other_name, ' ', Student.last_name).label('full_name'),
        Student.student_number,
        RoomType.price,
    ).join(Room, Booking.room_id == Room.id) \
        .join(RoomType, Room.room_type_id == RoomType.id) \
        .join(Block, Room.block_id == Block.id) \
        .join(Student, Booking.student_id == Student.id) \
        .filter(Student.id == user_id) \
        .all()


    bookings = []
    for result_tuple in my_booking:
        (id, room_name, room_type_name,
         block_name, status, paid,
         full_name, student_number, price) = result_tuple

        result_dict = {
            'id': id,
            'room_name': room_name,
            'room_type_name': room_type_name,
            'block_name': block_name,
            'status': status,
            'paid': float(paid),
            'full_name': full_name,
            'student_number': student_number,
            'price': float(price)
        }

        bookings.append(result_dict)

    return render_template('mybooking.html', bookings=bookings, user=user)


@student_views.route('/default/student/mybooking/details', methods=['GET'])
def booking_details():
    """ display student booking infor"""

    return render_template('details.html')
