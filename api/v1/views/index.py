#!/usr/bin/python3
""" API Blueprint  """
from flasgger import swag_from
from flask import request, abort
from sqlalchemy import and_

from api.v1.views import views
from models import storage
from models.booking import Booking
from models.student import Student
from api.v1.views.messaging import send_email
from flask import jsonify


@views.route('/status', methods=['GET'], strict_slashes=False)
@swag_from('documentation/index/get_status.yml')
def status():
    """ Returns status """
    return {"status": "OK"}, 200


@views.route('/unauthorized/', strict_slashes=False)
def unauthorized() -> None:
    """ GET unauthorized access error """
    abort(401)

@views.route('/forbidden/', strict_slashes=False)
def forbidden() -> None:
    """ GET forbidden access error """
    abort(403)


@views.route('/mail', methods=['POST'], strict_slashes=False)
@swag_from('documentation/index/post_mail.yml')
def mail_student():
    data = request.get_json()
    if (not data or 'level' not in data or 'not_paid'
            not in data or 'message' not in data):
        return jsonify({'error': 'Missing required data or data not in JSON format'}), 400

    level = data['level']
    not_paid = data['not_paid']
    message = data['message']
    student_email = []

    if level == 'All' and not_paid in ['Yes', 'No']:
        if not_paid == 'Yes':
            student_email = (storage.session.query(
                Student.email).filter(
                and_(Student.id == Booking.student_id,
                     Booking.status == 'pending')).join(Booking).all())
        else:
            student_email = storage.session.query(Student.email).all()
    else:
        student_email = storage.session.query(Student.email).join(Booking).filter(
            Booking.status == 'pending', Student.level == level
        ).all()

    if not student_email:
        return jsonify({'error': 'No matching students found'}), 400

    subject = "Notice from Academy Haven Hostel"

    for email_tuple in student_email:
        email = email_tuple[0]
        send_email(email, subject, message)

    return jsonify({'message': 'Emails sent successfully'}), 200
