#!/usr/bin/python3
""" setting up flask api """
from flask import Flask, request, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found_error(error):
    """ custom error 404 json message"""
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return (response)


if __name__ == '__main__':
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))

    app.run(host=host, port=port, threaded=True)
