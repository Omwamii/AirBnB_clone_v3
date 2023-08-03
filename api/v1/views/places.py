#!/usr/bin/python3
""" View to handle all Place objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.city import City
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/cities/<string:city_id>/places',
                 defaults={"place_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/places/<string:place_id>', defaults={"city_id": None},
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places(place_id, city_id):
    """ operate on Place objects
    """
    if request.method == "POST":
        try:
            api_req = request.get_json()
        except Exception:
            abort(400, description="Not a JSON")
        else:
            if 'name' not in api_req:
                abort(400, description="Missing name")
            elif 'user_id' not in api_req:
                abort(400, description="Missing user_id")
            else:
                # check if city_id is linked to any city obj
                city = storage.get(City, city_id)
                if city is None:
                    abort(404)
                # check if user_id is linked to any user
                user = storage.get(User, api_req['user_id'])
                if user is None:
                    abort(404)
                api_req['city_id'] = city_id

                # create place and return status 201
                obj = Place(**api_req)
                storage.new(obj)
                storage.save()
                return jsonify(obj.to_dict()), 201

    if request.method == "GET":
        if city_id is not None:
            # retrieve all place objs linked to city
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            linked_places = list()
            places = city.places
            for place in places:
                linked_places.append(place.to_dict())
            return jsonify(linked_places)
        else:
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            return jsonify(place.to_dict())
    if request.method == "DELETE":
        # try get the object with specific id
        place = storage.get(Place, place_id)
        # if place doesn't exist raise 404 error
        if place is None:
            abort(404)
        # if found delete object and return empty dict with status 200
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        # if place_id not linked to any place, raise 404
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        try:
            api_req = request.get_json()
        except Exception:
            # if not valid json raise 400 with 'Not a JSON'
            abort(400, description="Not a JSON")
        else:
            # update Place obj with the key-val pairs
            for key, val in api_req.items():
                if key not in ("id", "created_at", "updated_at",
                               "city_id", "user_id"):
                    setattr(place, key, val)
            storage.save()
            return jsonify(storage.get(Place, place_id).to_dict()), 200
