from flasgger import swag_from
from flask import jsonify, abort, request
from sqlalchemy import and_

from api.v1.views import views
from models import storage
from models.booking import Booking
from models.room import Room
from api.v1.views.messaging import send_email
from models.student import Student


def validate_booking_data(data):
    required_fields = ['room_id', 'student_id']
    for field in required_fields:
        if field not in data:
            return False, f"{field.replace('_', ' ').capitalize()} is missing"
    return True, None


@views.route('/bookings', methods=['GET'], strict_slashes=False)
@swag_from('documentation/booking/all_booking.yml')
def get_all_bookings():
    all_bookings = [booking.to_dict()
                    for booking in storage.all(Booking).values()]
    return jsonify(all_bookings)


@views.route('/booking/<booking_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/booking/get_booking.yml')
def get_booking_by_id(booking_id):
    booking = storage.get(Booking, booking_id)
    if not booking:
        abort(404)
    return jsonify(booking.to_dict())


@views.route('/booking/<booking_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/booking/delete_booking.yml')
def cancel_booking(booking_id):
    booking = storage.get(Booking, booking_id)
    if not booking:
        abort(404)
    room_id = booking.room_id
    room = storage.get(Room, room_id)
    booking.status = 'cancelled'
    room.booked_beds = int(room.booked_beds) - 1
    storage.session.commit()
    return jsonify({"cancelled": "success"})


@views.route('/booking', methods=['POST'], strict_slashes=False)
@swag_from('documentation/booking/post_booking.yml')
def create_booking():
    """Create a booking"""
    if not request.is_json:
        return jsonify({'error': 'Request data is not in JSON format'}), 400

    booking_data = request.get_json()
    is_valid, error_message = validate_booking_data(booking_data)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    room_id = booking_data.get('room_id')
    student_id = booking_data.get('student_id')

    existing_booking = storage.session.query(Booking).filter(
        and_(
            Booking.student_id == student_id,
            Booking.status == 'pending'
        )
    ).first()

    if existing_booking:
        return jsonify({'error': 'You have already booked a room'}), 400

    room = storage.get(Room, room_id)
    if room:
        if (room.no_of_beds - room.booked_beds - room.reserved_beds) == 0:
            return jsonify({'error': 'No available beds'}), 400

    new_booking = {
        'room_id': room_id,
        'student_id': student_id,
        'status': 'pending'
    }
    booking = Booking(**new_booking)
    booking.save()
    room.booked_beds += 1
    storage.session.commit()

    student = storage.get(Student, student_id)
    student_email = str(student.email)

    subject = 'Booking Successfully'
    body = (
        f'Dear {student.first_name} {student.last_name},\n\n'
        f'Congratulations! You have successfully booked {room.room_name} at Academy Haven Hostel.\n\n'
        f'Your booking is currently pending, and you have 24 hours to complete the payment.\n\n'
        f'Thank you for choosing Academy Haven Hostel for your stay.'
    )

    try:
        send_email(student_email, subject, body)
        return jsonify({'message': 'Booking created successfully'}), 201
    except Exception as e:
        print(f'Error sending email: {e}')
        return jsonify({'message': 'Booking created successfully'}), 201

