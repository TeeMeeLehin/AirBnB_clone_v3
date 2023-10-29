#!/usr/bin/python3
""" setting up api routes """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def status():
    """ route to get status of the api """
    response = {"status": "OK"}
    return (response)


@app_views.route('/stats')
def stats():
    """ route to get stats of storage objects """
    response = {}
    response["amenities"] = storage.count(Amenity)
    response["cities"] = storage.count(City)
    response["places"] = storage.count(Place)
    response["reviews"] = storage.count(Review)
    response["states"] = storage.count(State)
    response["users"] = storage.count(User)
    return (response)
