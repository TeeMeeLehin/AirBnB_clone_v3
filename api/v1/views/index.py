#!/usr/bin/python3
""" setting up api routes """
from api.v1.views import app_views


@app_views.route('/status')
def status():
    """ route to get status of the api """
    response = {"status": "OK"}
    return (response)
