#!/usr/bin/python3
""" api script for state objects """
from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


@app_views.route('/states', strict_slashes=False, methods=['GET'])
@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def states(state_id=None):
    """ returns list of states in storage """
    states = storage.all(State)
    if state_id is None:
        response = []
        for state in states.values():
            response.append(state.to_dict())
        return (jsonify(response))
    else:
        state = storage.get(State, state_id)
        if state is not None:
            return (jsonify(state.to_dict()))
        else:
            abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id):
    """ deletes a state object """
    state = storage.get(State, state_id)
    if state is not None:
        storage.delete(state)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """ create a new state """
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")

    if "name" not in state_data:
        abort(400, "Missing name")

    new_state = State(**state_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """ update a state object """
    state = storage.get(State, state_id)
    state_data = request.get_json()
    if state_data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key in keys_to_ignore:
        if key in state_data:
            del state_data[key]

    for key, value in state_data.items():
        setattr(state, key, value)
    state.save()

    return jsonify(state.to_dict()), 200
