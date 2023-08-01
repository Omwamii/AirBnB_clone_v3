#!/usr/bin/python3
""" route mapping
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def status():
    """ return the status of the API
    """
    status = {"status": "OK"}
    return jsonify(status)

@app_views.route('/stats', methods=['GET'])
def stats():
    """ return the number of objects in storage
    """
    obj_map = {
            "amenities": "Amenity",
            "cities": "City",
            "places": "Place",
            "reviews": "Review",
            "states": "State",
            "users": "User"
            }
    stats = dict()
    for key, val in obj_map.items():
        stats[key] = storage.count(val)
    return jsonify(stats)
