#!/usr/bin/env python3
import bcrypt
from sqlalchemy import func, and_
from models.booking import Booking
from models.student import Student
from web_flask.forms.password import ChangePasswordForm
from web_flask.forms.student import StudentForm
from web_flask.student_model import student_views
from flask import render_template, session, redirect, url_for, request
from models import storage
from models.room import Room
from models.block import Block
from models.room_type import RoomType


@student_views.route('/', methods=['GET', 'POST'])
def default():
    """
    This function handles the default route for the student views.

    It renders the 'Sdefault.html' template and handles the form submission.
    If the request method is POST, it checks the submitted email and password
    against the stored user data. If the credentials are valid, it sets the
    user_id and user session variables and redirects to the dashboard. If the
    credentials are invalid, it sets an error message. If an exception occurs,
    it sets a generic error message.

    Returns:
        The rendered template 'Sdefault.html' with the form and error_message
        variables passed to it.
    """
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
    """
    Logs out the student by clearing the session and redirecting to the default page.

    Returns:
        A redirect response to the default page.
    """
    if 'user_id' in session:
        session.clear()
    return redirect(url_for('student_views.default'))


@student_views.route('/default/student', methods=['GET'])
def dashboard():
    """Render the student dashboard page.

    This function checks if the user is logged in and redirects to the default page if not.
    It retrieves information about available rooms and displays them on the dashboard.

    Returns:
        A rendered template of the student dashboard page with the following variables:
        - blocks: A list of all blocks.
        - room_types: A list of all room types.
        - rooms: A list of dictionaries containing information about available rooms.
    """
    if 'user_id' not in session:
        return redirect(url_for('student_views.default'))
    else:
        block = storage.all(Block).values()
        blocks = [block.to_dict() for block in block]
        room_types = storage.all(RoomType).values()
        room_type = [room_type.to_dict() for room_type in room_types]
        user_id = session['user_id']
        user = storage.get(Student, user_id)
        gender = user.gender

        room = (storage.session.query(
            Room.id, Room.room_name,
            (Room.no_of_beds - Room.booked_beds -
             Room.reserved_beds).label('available_beds') ,
            Room.floor, Room.gender,
            RoomType.name.label('room_type_name'), RoomType.price,
            Block.name.label('block_name'))
            .join(Block, Room.block_id == Block.id)
            .join(RoomType, Room.room_type_id == RoomType.id)
            .filter(and_((Room.no_of_beds - Room.booked_beds -
             Room.reserved_beds) > 0,
                         Room.gender == gender)).all())

        rooms = []
        for result_tuple in room:
            (id, room_name, available_beds, floor,
             gender, room_type_name, price,
             block_name) = result_tuple

            result_dict = {
                'id': id,
                'room_name': room_name,
                'available_beds': available_beds,  # Use the calculated available_beds
                'floor': floor,
                'gender': gender,
                'room_type_name': room_type_name,
                'price': price,
                'block_name': block_name
            }

            rooms.append(result_dict)

       # print(rooms)

    return render_template('Sbase.html',
                           blocks=block,
                           room_types=room_type,
                           rooms=rooms)


@student_views.route('/default/student/profile', methods=['GET'])
def student_profile():
    """Renders the student profile page.

    This function retrieves the user's information from the session and populates the student profile form with the data.
    If the user is not logged in, they will be redirected to the default page.

    Returns:
        A rendered template of the student profile page with the populated form and user information.
    """
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
            form.first_name.data = user['first_name'] if user.get(
                'first_name') is not None else ""
            form.last_name.data = user['last_name'] if 'last_name' in user else ""
            form.other_name.data = user['other_name'] if 'other_name' in user else ""
            form.email.data = user['email'] if 'email' in user else ""
            form.phone.data = user['phone'] if 'phone' in user else ""
            form.student_number.data = user['student_number'] if 'student_number' in user else ""
            form.program.data = user['program'] if 'program' in user else ""
            form.level.data = user['level'] if 'level' in user else ""
            form.guardian_name.data = user['guardian_name'] if 'guardian_name' in user else ""
            form.guardian_phone.data = user['guardian_phone'] if 'guardian_phone' in user else ""
            form.disability.data = user['disability'] if 'disability' in user else ""
            form.gender.data = user['gender'] if 'gender' in user else ""
            form.address.data = user['address'] if 'address' in user else ""
            form.date_of_birth.data = user['date_of_birth'] if 'date_of_birth' in user else ""
        except Exception as e:
            pass

    return render_template('Sprofile.html',
                           form=form, user=user, reset=reset)


@student_views.route('/default/student/mybooking', methods=['GET'])
def my_bookings():
    """Display student booking information.

    This function retrieves the booking information for a student and renders it on the 'mybooking.html' template.
    It first checks if the 'user_id' is present in the session. If not, it redirects to the 'default' view.
    Then, it retrieves the user object from the database based on the 'user_id'.
    If the user object does not exist, it redirects to the 'default' view.
    It then performs a query to fetch the booking information for the student, including the room details, block details,
    and student details.
    The query results are processed and stored in a list of dictionaries, where each dictionary represents a booking.
    Finally, it renders the 'mybooking.html' template with the bookings and user objects as context variables.

    Returns:
        The rendered 'mybooking.html' template with the bookings and user objects as context variables.
    """
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
        func.concat(Student.first_name, ' ', Student.other_name,
                    ' ', Student.last_name).label('full_name'),
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
