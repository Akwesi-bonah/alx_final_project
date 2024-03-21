#!/usr/bin/python3
""" API Blueprint  for Room"""
from flasgger import swag_from

from api.v1.views import views
from flask import jsonify, abort, request
from models.room import Room
from models import storage


def validate_room_data(data):
    """validate required fields"""
    required_fields = ['room_name', 'room_type_id',
                       'gender',
                       'block_id']

    for field in required_fields:
        if field not in data:
            return False, f"{field.capitalize().replace('_', ' ')} is missing"

    return True, None


@views.route('/rooms', methods=['GET'], strict_slashes=False)
@swag_from('documentation/room/all_room_get.yml')
def room():
    """ Get all rooms """
    all_rooms = storage.all(Room).values()
    rooms = [room.to_dict() for
             room in all_rooms]
    return jsonify(rooms)


@views.route('/room/<room_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/room/get_room.yml')
def get_room(room_id):
    """ Get room by id """
    room = storage.get(Room, room_id)
    if not room:
        abort(404)
    return jsonify(room.to_dict())


@views.route('/room/<room_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/room/delete_room.yml')
def delete_room(room_id):
    """ Delete room by id """
    room = storage.get(Room, room_id)
    if not room:
        abort(404)
    storage.delete(room)
    storage.save()
    return jsonify({})


@views.route('/room', methods=['POST'], strict_slashes=False)
@swag_from('documentation/room/post_room.yml')
def add_room():
    """ Create new room """
    if not request.get_json():
        return jsonify({'error': 'Not JSON'}), 400

    is_valid, error_message = validate_room_data(request.get_json())
    if not is_valid:
        return jsonify({'error': error_message}), 400

    check_name = storage.session.query(Room).filter_by(
        room_name=request.get_json()['room_name']).first()
    if check_name:
        return jsonify({'error': 'Room name already exists'}), 400

    try:
        data = request.get_json()
        instance = Room(**data)
        instance.save()
        return jsonify(instance.to_dict())
    except Exception as e:
        return jsonify({'error': e}), 400


@views.route('/room/<room_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/room/put_room.yml')
def update_room(room_id):
    """ Update room by id """
    room = storage.get(Room, room_id)
    if not room:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    ignore = ['id', 'created_at', 'updated_at']
    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(room, key, value)
    room.save()
    return jsonify(room.to_dict())
