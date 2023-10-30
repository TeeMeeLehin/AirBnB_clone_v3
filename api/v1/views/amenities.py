#!/usr/bin/python3
""" api script for state objects """
from api.v1.views import app_views
from models.city import City
from models.state import State
from models.amenity import Amenity
from models import storage
from flask import jsonify, abort, request


@app_views.route('/amenities', strict_slashes=False, methods=['GET'])
@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenities(amenity_id):
    """ returns list of amenities in storage """
    amenities = storage.all(Amenity)
    if amenity_id is None:
        response = []
        for amenity in amenities.values():
            response.append(amenity.to_dict())
        return jsonify(response)
    else:
        amenity = storage.get(Amenity, amenity_id)
        if amenity is not None:
            return jsonify(amenity.to_dict())
        else:
            abort(400)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    """ deletes a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is not None:
        storage.delete(amenity)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    """ create a new amenity """
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")

    if "name" not in amenity_data:
        abort(400, "Missing name")

    new_amenity = Amenity(**amenity_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(city_id):
    """ update a amenity object """
    amenity = storage.get(Amenity, amenity_id)
    amenity_data = request.get_json()
    if amenity_data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key in keys_to_ignore:
        if key in amenity_data:
            del amenity_data[key]

    for key, value in amenity_data.items():
        setattr(amenity, key, value)
    amenity.save()

    return jsonify(amenity.to_dict()), 200
