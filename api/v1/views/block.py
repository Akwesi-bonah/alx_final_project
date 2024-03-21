#!/usr/bin/python3
"""" API Blueprint for Block """

from models.block import Block
from models import storage
from api.v1.views import views
from flask import jsonify, abort, request
from flasgger.utils import swag_from


def validate_block_data(data):
    """validate required fields"""
    required_fields = ['campus', 'name',
                       'description']

    for field in required_fields:
        if field not in data:
            return False, f"{field.capitalize().replace('_', ' ')} is missing"

    return True, None


@views.route('/blocks', methods=['GET'], strict_slashes=False)
@swag_from('documentation/block/all_block.yml')
def get_blocks():
    """ Retrieves the list of all Student objects """
    all_block = storage.all(Block).values()
    block = [block.to_dict() for block in all_block]
    return jsonify(block)


@views.route('/block/<block_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/block/get_block.yml')
def get_block(block_id):
    """Retrieves a block"""
    block = storage.get(Block, block_id)
    if not block:
        abort(404, description="Not Found")
    return jsonify(block.to_dict())


@views.route('/block/<block_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/block/delete_block.yml')
def delete_block(block_id):
    """Delete block object"""
    block = storage.get(Block, block_id)
    if not block:
        abort(404)
    storage.delete(block)
    storage.save()
    return jsonify({})


@views.route('/block', methods=['POST'], strict_slashes=False)
@swag_from('documentation/block/post_block.yml')
def add_block():
    """create new block object"""

    if not request.get_json():
        return jsonify({'error': 'Not'}), 400

    is_valid, error_message = validate_block_data(request.get_json())
    if not is_valid:
        return jsonify({'error': error_message}), 400

    check_name = request.get_json()['name']
    if storage.session.query(Block).filter_by(name=check_name).first():
        return jsonify({'error': 'Name already exist'}), 400

    data = request.get_json()
    try:
        instance = Block(**data)
        instance.save()
        return jsonify(instance.to_dict(), 201)
    except Exception as e:
        return jsonify({'Error': "some Error Occurred"})


@views.route('/block/<block_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/block/put_block.yml')
def update_block(block_id):
    """update block object"""

    block = storage.get(Block, block_id)
    if not block:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key not in ignore:
            setattr(block, key, value)
    storage.save()
    return jsonify(block.to_dict())
