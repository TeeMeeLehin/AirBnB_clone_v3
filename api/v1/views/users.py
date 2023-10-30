#!/usr/bin/python3
""" api script for state objects """
from api.v1.views import app_views
from models.user import User
from models import storage
from flask import jsonify, abort, request


@app_views.route('/users', strict_slashes=False, methods=['GET'])
@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET'])
def users(user_id=None):
    """ returns list of users in storage """
    users = storage.all(User)
    if user_id is None:
        response = []
        for user in users.values():
            response.append(user.to_dict())
        return jsonify(response)
    else:
        user = storage.get(User, user_id)
        if user is not None:
            return jsonify(user.to_dict())
        else:
            abort(404)


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_users(user_id):
    """ deletes a user object """
    user = storage.get(User, user_id)
    if user is not None:
        storage.delete(user)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """ create a new user """
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")

    if "name" not in user_data:
        abort(400, "Missing name")

    new_user = User(**user_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    """ update a user object """
    user = storage.get(User, user_id)
    user_data = request.get_json()
    if user_data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "created_at", "updated_at"]
    for key in keys_to_ignore:
        if key in user_data:
            del user_data[key]

    for key, value in user_data.items():
        setattr(user, key, value)
    user.save()

    return jsonify(user.to_dict()), 200
