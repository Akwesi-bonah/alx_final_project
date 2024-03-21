#!/usr/bin/python3
"""" API Blueprint for staff """
from flasgger import swag_from

from models import storage
from models.staff import Staff
from api.v1.views import views
from flask import jsonify, abort, request, make_response


def validate_staff_data(data):
    """validate required fields"""
    required_fields = ['name', 'email', 'password', 'role', 'status', 'phone']

    for field in required_fields:
        if field not in data:
            return False, f"{field.capitalize().replace('_', ' ')} is missing"

    return True, None


@views.route('/staffs', methods=['GET'], strict_slashes=False)
@swag_from('documentation/staff/all_staff.yml')
def get_staffs():
    """ Retrieves the list of all Staff objects """
    all_staff = storage.all(Staff).values()
    staff = [staff.to_dict() for staff in all_staff]
    return jsonify(staff)


@views.route('/staff/<staff_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/staff/get_staff.yml')
def get_staff(staff_id):
    """Retrieves a staff"""

    staff = storage.get(Staff, staff_id)
    if not Staff:
        return jsonify({"error ": "Staff Not Found"})

    return jsonify(staff.to_dict())


@views.route('/staff/<staff_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/staff/delete_staff.yml')
def delete_staff(staff_id):
    """Delete staff object"""
    staff = storage.get(Staff, staff_id)

    if staff:
        storage.delete(staff)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        return make_response(jsonify({'error': 'Staff not found'}), 404)


@views.route('/staff', methods=['POST'], strict_slashes=False)
@swag_from('documentation/staff/post_staff.yml')
def add_staff():
    """create new staff object"""

    if not request.get_json():
        return jsonify({'error': 'Not JSON'}), 400

    is_valid, error_message = validate_staff_data(request.get_json())
    if not is_valid:
        return jsonify({'error': error_message}), 400

    email = request.get_json()['email']
    staff = storage.get_user_email(email)
    if staff:
        return jsonify({'error': 'Email already exists'}), 400

    Dphone = request.get_json()['phone']
    phone = storage.get_user_phone(Dphone)
    if phone:
        return jsonify({'error': 'Phone already exists'}), 400

    try:
        data = request.get_json()
        instance = Staff(**data)
        instance.save()
        return make_response(jsonify(instance.to_dict()), 201)
    except Exception as e:
        abort(400, description=" Error Occurred  email or phone already exist")


@views.route('/staff/<staff_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/staff/put_staff.yml')
def update_staff(staff_id):
    """Update a staff"""

    if not request.get_json():
        abort(400, description="Not a JSON")

    staff = storage.get(Staff, staff_id)
    if not Staff:
        abort(400, description="Staff Not Found")

    ignore = ['id',  'created_at', 'updated_at']

    data = request.get_json()
    try:
        for key, value in data.items():
            if key not in ignore:
                setattr(staff, key, value)
        storage.save()
        return make_response(jsonify(staff.to_dict()), 200)
    except Exception as e:
        return jsonify({"error": " Error Occurred"})
