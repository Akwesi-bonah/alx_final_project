#!/usr/bin/python3
"""This module defines the Reservation view"""
from flasgger import swag_from

from api.v1.views import views
from flask import jsonify, request
from models.room import Room
from models import storage


def validate_reservation_data(data):
    """validate required fields"""
    required_fields = ['room_id', 'no_of_beds']

    for field in required_fields:
        if field not in data:
            return False, f"{field.capitalize().replace('_', ' ')} is missing"

    return True, None


@views.route('/fetch', methods=['GET'], strict_slashes=False)
@swag_from('documentation/reservation/get_fetch.yml')
def fetch():
    """ Fetch rooms based on block and room type """
    block_id = request.args.get('block_id')
    room_type_id = request.args.get('room_type_id')

    if not block_id or not room_type_id:
        return jsonify({'error': 'Both Block and Room Type ID required'}), 400

    rooms_fetched = storage.session.query(
        Room.id, Room.room_name, Room.booked_beds
    ).filter(
        Room.block_id == block_id,
        Room.room_type_id == room_type_id
    ).all()

    rooms_list = []
    for result_tuple in rooms_fetched:
        room_id, room_name, booked_beds = result_tuple

        room_dict = {
            'id': room_id,
            'room_name': room_name,
            'booked_beds': booked_beds
        }

        rooms_list.append(room_dict)

    return jsonify({'rooms': rooms_list})


@views.route('/reserve', methods=['POST'], strict_slashes=False)
@swag_from('documentation/reservation/post_reservation.yml')
def reserve_room():
    """Reserve a room"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    valid_data, message = validate_reservation_data(data)
    if not valid_data:
        return jsonify({'error': message}), 400

    room_id = data.get('room_id')
    if not room_id:
        return jsonify({'error': 'Room ID required'}), 400

    beds = data.get('no_of_beds')
    if not beds:
        return jsonify({'error': 'Number of beds Required'}), 400

    room = storage.get(Room, room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404

    current_beds = int(room.no_of_beds) - int(room.reserved_beds) - int(room.booked_beds) - int(beds)
    status = "Available"
    if current_beds <= 0:
        return jsonify({'error': 'Cannot reserve more beds than available'}), 400
    else:
        if current_beds == 0:
            status = "Full"
        room.reserved_beds += int(beds)
        room.status = status
        storage.session.commit()
        return jsonify({'message': 'Room successfully reserved'}), 200


@views.route('/cancel', methods=['POST'], strict_slashes=False)
@swag_from('documentation/reservation/post_cancel.yml')
def cancel_reservation():
    """Cancel a reservation"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'Not a JSON'}), 400

    valid_data, message = validate_reservation_data(data)
    if not valid_data:
        return jsonify({'error': message}), 400

    room_id = data.get('room_id')
    if not room_id:
        return jsonify({'error': 'Room ID required'}), 400

    beds = data.get('no_of_beds')
    if not beds:
        return jsonify({'error': 'Number of beds Required'}), 400

    room = storage.get(Room, room_id)
    if not room:
        return jsonify({'error': 'Room not found'}), 404
    
    current_beds = int(room.no_of_beds) - int(room.reserved_beds) - int(room.booked_beds) - int(beds)
    status = "Available"

    if current_beds <= 0:
        return jsonify({'error': 'Cannot cancel more beds than reserved'}), 400
    else:
        if current_beds == 0:
            status = "Full"
        room.reserved_beds -= int(beds)
        room.status = status
        storage.session.commit()
        return jsonify({'message': 'Room successfully reserved'}), 200
