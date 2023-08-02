#!/usr/bin/python3
""" View to handle all State objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<string:state_id>/cities',
                 defaults={"city_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/cities/<string:city_id>', defaults={"state_id": None},
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def cities(state_id, city_id):
    """ operate on City objects
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
                state = storage.get(State, state_id)
                if state is None:
                    abort(404)
                api_req['state_id'] = state_id
                obj = City(**api_req)
                storage.new(obj)
                storage.save()
                return jsonify(obj.to_dict()), 201

    if request.method == "GET":
        if state_id is not None:
            # retrieve State object with id
            state = storage.get(State, state_id)
            if state is None:
                abort(404)
            linked_cities = list()
            cities = state.cities
            for city in cities:
                linked_cities.append(city.to_dict())
            return jsonify(linked_cities)
        else:
            city = storage.get(City, city_id)
            if city is None:
                abort(404)
            return jsonify(city.to_dict())
    if request.method == "DELETE":
        # try get the object with specific id
        city = storage.get(City, city_id)
        # if city doesn't exist raise 404 error
        if city is None:
            abort(404)
        # if found delete object and return empty dict with status 200
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        # if city_id not linked to any city, raise 404
        city = storage.get(City, city_id)
        if city is None:
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
                    setattr(city, key, val)
            storage.save()
            return jsonify(storage.get(City, city_id).to_dict()), 200
