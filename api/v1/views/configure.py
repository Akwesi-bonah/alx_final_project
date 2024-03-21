from datetime import datetime

from flasgger import swag_from

from api.v1.views import views
from models import storage
from models.booking import Booking
from models.configuration import Configuration
from flask import request, jsonify

from models.room import Room


@views.route('/configure', methods=['POST'])
@swag_from('documentation/configure/post_configure.yml')
def set_configuration():
    """Set new configuration"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Not JSON'})

    required_fields = ['created_by', 'expiry_date', 'start_date']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({'error': f"{', '.join(missing_fields)} is missing"}), 400

    start_date = data['start_date']

    try:
            old_bookings = storage.session.query(Booking).filter(
                Booking.created_at < start_date).all()

            for booking in old_bookings:
                if booking.status != 'expired':
                    booking.status = 'expired'

            rooms = storage.session.query(Room).all()
            for room in rooms:
                room.booked_beds = 0
                room.reserved_beds = 0

            storage.session.commit()

            new_config = Configuration(created_by=data['created_by'], expiry_date=data['expiry_date'])
            new_config.save()
            return jsonify({'message': 'Configuration set successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
