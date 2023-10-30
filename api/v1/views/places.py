#!/usr/bin/python3
""" api script for state objects """
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET'])
def city_places(city_id):
    """ returns list of places of a city """
    places = storage.all(Place)
    city = storage.get(City, city_id)
    if city is not None:
        response = []
        for place in city.places:
            response.append(place.to_dict())
        return jsonify(response)
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['GET'])
def places(place_id):
    """ returns a place in storage """
    place = storage.get(Place, place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    """ deletes a place object """
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    """ create a new place """
    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")

    if "name" not in place_data:
        abort(400, "Missing name")

    new_place = Place(**place_data)
    new_place.city_id = city_id
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', strict_slashes=False, methods=['PUT'])
def update_place(place_id):
    """ update a place object """
    place = storage.get(Place, place_id)
    place_data = request.get_json()
    if place_data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key in keys_to_ignore:
        if key in place_data:
            del place_data[key]

    for key, value in place_data.items():
        setattr(place, key, value)
    place.save()

    return jsonify(place.to_dict()), 200
