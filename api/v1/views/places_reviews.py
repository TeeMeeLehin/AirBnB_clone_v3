#!/usr/bin/python3
""" api script for state objects """
from api.v1.views import app_views
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
from flask import jsonify, abort, request


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def places_reviews(place_id):
    """ returns list of reviews of a place """
    reviews = storage.all(Review)
    place = storage.get(Place, place_id)
    if place is not None:
        response = []
        for review in place.reviews:
            response.append(review.to_dict())
        return jsonify(response)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def reviews(review_id):
    """ returns a review in storage """
    review = storage.get(Review, review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """ deletes a review object """
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    """ create a new review """
    review_data = request.get_json()
    places = storage.all(Place)
    users = storage.all(User)
    if review_data is None:
        abort(400, "Not a JSON")

    if "name" not in review_data:
        abort(400, "Missing name")

    if "user_id" not in review_data:
        abort(400, "Missing user_id")

    place_key = "Place.{}".format(place_id)
    if place_key not in places:
        abort(404)

    user_key = "User.{}".format(place_data['user_id'])
    if user_key not in users:
        abort(404)

    new_review = Review(**review_data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(place_id):
    """ update a review object """
    review = storage.get(Review, review_id)
    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")

    keys_to_ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key in keys_to_ignore:
        if key in review_data:
            del review_data[key]

    for key, value in review_data.items():
        setattr(review, key, value)
    review.save()

    return jsonify(review.to_dict()), 200
