#!/usr/bin/python3
""" api script for state objects """
from api.v1.views import app_views
from models.city import City
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def state_cities(state_id):
    """ returns list of cities of a state """
    states = storage.all(State)
    state = storage.get(State, state_id)
    if state is not None:
        response = []
        for city in state.cities:
            response.append(city.to_dict())
        return jsonify(response)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def cities(city_id):
    """ returns a city in storage """
    city = storage.get(City, city_id)
    if city is not None:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    """ deletes a city object """
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city():
    """ create a new city """
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")

    if "name" not in city_data:
        abort(400, "Missing name")

    new_city = City(**city_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_state(city_id):
    """ update a city object """
    city = storage.get(City, city_id)
    city_data = request.get_json()
    if city_data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key in keys_to_ignore:
        if key in city_data:
            del city_data[key]

    for key, value in city_data.items():
        setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
