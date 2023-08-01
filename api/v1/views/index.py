#!/usr/bin/python3
""" route mapping
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ return the status of the API
    """
    status = {
            "status": "OK"
            }
    return jsonify(status)
