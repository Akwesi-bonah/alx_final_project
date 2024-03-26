#!/usr/bin/python3
"""" API Blueprint for students """
import os
from datetime import datetime

from flasgger import swag_from
from werkzeug.utils import secure_filename

from models.student import Student
from models import storage
from api.v1.views import views
from flask import jsonify, abort, request, make_response


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


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/students', methods=['GET'], strict_slashes=False)
@swag_from('documentation/student/all_student.yml')
def get_students():
    """ Retrieves the list of all Student objects """
    try:
        students = storage.all(Student).values()
        students = [student.to_dict() for student in students]
        return jsonify(students)
    except Exception as e:
        return jsonify({"error": str(e)})


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
    """Add new student"""
    request_data = request.form.to_dict()

    if not request_data:
        return jsonify({'error': 'Not JSON'}), 400

    is_valid, error_message = validate_student_data(request_data)
    if not is_valid:
        return jsonify({'error': error_message}), 400

    check_email = request_data.get('email')
    if storage.find_by(Student, email=check_email):
        return jsonify({'error': 'Email already exists'}), 400

    check_phone = request_data.get('phone')
    if storage.find_by(Student, phone=check_phone):
        return jsonify({'error': 'Phone already exists'}), 400

    student_number = request_data.get('student_number')
    if storage.find_by(Student, student_number=student_number):
        return jsonify({'error': 'Student number already exists'}), 400

    if 'profile_picture' in request.files:
        image = request.files['profile_picture']
        if image.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(image.filename):
            return jsonify({'error': 'Invalid file format'}), 400
        if image.content_length > MAX_FILE_SIZE:
            return jsonify({'error': 'File size exceeds the limit'}), 400

        uploads_folder = "students_profile"
        os.makedirs(uploads_folder, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        filename = f"{timestamp}_{secure_filename(image.filename)}"

        image_path = os.path.join(uploads_folder, secure_filename(filename))
        image.save(image_path)
        request_data['profile_picture'] = image_path

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


@views.route('/student/image/<student_id>', methods=['GET'], strict_slashes=False)
def image(student_id):
    try:
        student = storage.get(Student, student_id)
        if not student:
            return jsonify({"error": "Student Not Found"}), 404

        # Get the path to the profile picture from the student object
        profile_picture_path = student.profile_picture
        if profile_picture_path is None:
            return jsonify({"error": "not picture found"})

        # Check if the file exists
        if not os.path.exists(profile_picture_path):
            return jsonify({"error": "Profile picture not found"}), 404

        # Open the file and send it as a response
        with open(profile_picture_path, 'rb') as file:
            image_data = file.read()

        # Set the appropriate content type for the image
        response = make_response(image_data)
        response.headers['Content-Type'] = 'image/*'
        return response

    except Exception as e:
        return jsonify({'error': str(e)}), 500
