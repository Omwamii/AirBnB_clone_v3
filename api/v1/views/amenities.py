#!/usr/bin/python3
""" View to handle all Amenity objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', defaults={"amenity_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/amenities/<string:amenity_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def states(amenity_id):
    """ operate on State objects
    """
    if request.method == "POST":
        try:
            api_req = request.get_json()
        except Exception:
            abort(400, description="Not a JSON")
        else:
            if 'name' not in api_req:
                abort(400, description="Missing name")
            else:
                # create object and return status code 201
                obj = Amenity(**api_req)
                storage.new(obj)
                storage.save()
                return jsonify(obj.to_dict()), 201

    if request.method == "GET":
        if amenity_id is None:
            # return all Amenity objects
            all_amenities = storage.all(Amenity)
            amenities = list()
            for val in all_amenities.values():
                amenities.append(val.to_dict())
            return jsonify(amenities)
        else:
            # get state with specific amenity_id
            obj = storage.get(Amenity, amenity_id)
            if obj is None:
                abort(404)
            return jsonify(obj.to_dict())
    if request.method == "DELETE":
        # try get the object with specific id
        obj = storage.get(Amenity, amenity_id)
        # if object doesn't exist raise 404 error
        if obj is None:
            abort(404)
        # if found delete object and return empty dict with status 200
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        # if state_id not linked to any State, raise 404
        obj = storage.get(Amenity, amenity_id)
        if obj is None:
            abort(404)
        try:
            api_req = request.get_json()
        except Exception:
            # if not valid json raise 400 with 'Not a JSON'
            abort(400, description="Not a JSON")
        else:
            # update State obj with the key-val pairs
            for key, val in api_req.items():
                if key not in ("id", "created_at", "updated_at"):
                    setattr(obj, key, val)
            storage.save()
            return jsonify(storage.get(Amenity, amenity_id).to_dict()), 200
