#!/usr/bin/python3
""" API Blueprint  for Payment"""
from flasgger import swag_from
from sqlalchemy import func

from api.v1.views import views
from flask import jsonify, request
from api.v1.views.messaging import send_email
from models.booking import Booking
from models.room import Room
from models import storage
from models.payment import Payment
from models.room_type import RoomType
from models.student import Student


@views.route('/paymentInfo/<booking_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/payment/payment_infor.yml')
def payment(booking_id):
    """ Get all payments """

    if booking_id is None:
        return jsonify({'error': 'booking_id is missing'}), 400

    booking_info = storage.session.query(
        Booking.room_id,
        Booking.student_id,
        Booking.paid,
        Booking.status,
        func.concat(Student.first_name, ' ',
                    Student.last_name).label('student_name'),
        Student.email,
        Room.room_name,
        RoomType.name,
        RoomType.price
    ).filter(
        Booking.id == booking_id,
        Booking.status == 'pending'
    ).join(
        Room, Room.id == Booking.room_id
    ).join(
        RoomType, RoomType.id == Room.room_type_id
    ).join(
        Student, Student.id == Booking.student_id

    ).first()

    if not booking_info:
        return jsonify({'error': 'No pending booking '
                                 'found for the provided booking_id'}), 400

    booking_dict = {
        'room_id': booking_info[0],
        'student_id': booking_info[1],
        'paid': booking_info[2],
        'status': booking_info[3],
        'student_name': booking_info[4],
        'student_email': booking_info[5],
        'room_name': booking_info[6],
        'room_type_name': booking_info[7],
        'room_type_price': booking_info[8]
    }

    return jsonify({'booking_info': booking_dict})


@views.route('/payment', methods=['POST'], strict_slashes=False)
@swag_from('documentation/payment/post_payment.yml')
def add_payment():
    """ Add a new payment """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not JSON'}), 400

    required_fields = ['booking_id', 'amount', 'student_id', 'reference_id']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f"{', '.join(missing_fields)} is missing"}), 400

    booking_id = data['booking_id']
    amount = data['amount']
    student_id = data['student_id']
    reference_id = data['reference_id']

    student = storage.get(Student, student_id)
    student_email = str(student.email)

    booking = storage.get(Booking, booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    room_type_price = float(data['room_type_price'])

    booking.paid = float(booking.paid) + float(amount)
    booking.status = 'paid' if float(booking.paid) >= room_type_price else 'pending'
    storage.session.commit()

    new_payment = Payment(booking_id=booking_id, amount=amount,
                          student_id=student_id,
                          reference_id=reference_id)
    new_payment.save()

    try:
        subject = f'Payment Confirmation for Booking ID {booking_id}'
        body = (f'Dear {student.first_name} {student.last_name},\n\n'
                f'An amount of GHC {amount} has been paid for your booking (Booking ID: {booking_id}).'
                f'\n\nYour booking balance is GHC {room_type_price - amount}.\n\nThank you for your payment!')
        send_email(student_email, subject, body)
    except Exception as e:
        print(jsonify({'error': f'Error sending email: {str(e)}'}), 5000)

    return jsonify(new_payment.to_dict()), 201
