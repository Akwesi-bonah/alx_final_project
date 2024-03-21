#!/usr/bin/python3
"""" API Blueprint for students """
from flasgger import swag_from

from models.student import Student
from models import storage
from api.v1.views import views
from flask import jsonify, abort, request


# Validation for required fields
def validate_student_data(data):
    """validate required fields"""
    required_fields = ['first_name', 'last_name',
                       'date_of_birth', 'gender',
                       'student_number',
                       'email', 'phone']

    for field in required_fields:
        if field not in data:
            return False, f"{field.capitalize().replace('_', ' ')} is missing"

    return True, None


@views.route('/students', methods=['GET'], strict_slashes=False)
@swag_from('documentation/student/all_student.yml')
def get_students():
    """ Retrieves the list of all Student objects """
    students = storage.all(Student).values()
    students = [student.to_dict() for student in students]
    return jsonify(students)


@views.route('/student/<student_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/student/get_student.yml')
def get_student(student_id):
    """Retrieves a student"""
    student = storage.get(Student, student_id)
    if not student:
        return jsonify({"error ": "Student Not Found"})
    return jsonify(student.to_dict())


@views.route('/student/<student_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/student/delete_student.yml')
def delete_student(student_id):
    """Deletes a student"""
    student = storage.get(Student, student_id)
    if not student:
        abort(404)
    storage.delete(student)
    storage.save()
    return jsonify({})


@views.route('/student', methods=['POST'], strict_slashes=False)
@swag_from('documentation/student/post_student.yml')
def add_student():
    """ Add new student"""
    request_data = request.get_json()

    if not request_data:
        return jsonify({'error': 'Not JSON'}), 400

    is_valid, error_message = validate_student_data(request_data)
    if not is_valid:
        return jsonify({'error': error_message}), 400
    check_email = request_data.get('email')
    if storage.session.query(Student).filter_by(
            email=check_email).first():
        return jsonify({'error': 'Email already exists'}), 400
    check_phone = request_data.get('phone')
    if storage.session.query(Student).filter_by(
            phone=check_phone).first():
        return jsonify({'error': 'Phone already exists'}), 400
    student_number = request_data.get('student_number')
    check_number = storage.session.query(Student).filter_by(
        student_number=student_number).first()
    if check_number:
        return jsonify({'error': 'Student number already exists'}), 400
    try:
        new_student = Student(**request_data)
        new_student.save()
        return jsonify(new_student.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@views.route('/student/<student_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/student/put_student.yml')
def update_student(student_id):
    """Updates a student"""
    student = storage.get(Student, student_id)
    if not student:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(student, key, value)
    storage.save()
    return jsonify(student.to_dict()), 200
