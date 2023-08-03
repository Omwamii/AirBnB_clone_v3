#!/usr/bin/python3
""" View to handle all State objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.state import State
from models import storage


@app_views.route('/states', defaults={"state_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<string:state_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def states(state_id):
    """ operate on State objects
    """
    if request.method == "POST":
        api_req = request.get_jon()
        if api_req is None:
            abort(400, description="Not a JSON")
        if 'name' not in api_req:
            abort(400, description="Missing name")
        else:
            # create object and return status code 201
            obj = State(**api_req)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201

    if request.method == "GET":
        if state_id is None:
            # return all state objects
            all_states = storage.all(State)
            state_data = list()
            for val in all_states.values():
                state_data.append(val.to_dict())
            return jsonify(state_data)
        else:
            # get state with specific state_id
            obj = storage.get(State, state_id)
            if obj is None:
                abort(404)
            return jsonify(obj.to_dict())
    if request.method == "DELETE":
        # try get the object with specific id
        obj = storage.get(State, state_id)
        # if object doesn't exist raise 404 error
        if obj is None:
            abort(404)
        # if found delete object and return empty dict with status 200
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        # if state_id not linked to any State, raise 404
        obj = storage.get(State, state_id)
        if obj is None:
            abort(404)
        api_req = request.get_json()
        if api_req is None:
            abort(400, description="Not a JSON")
        else:
            # update State obj with the key-val pairs
            for key, val in api_req.items():
                if key not in ("id", "created_at", "updated_at"):
                    setattr(obj, key, val)
            storage.save()
            return jsonify(storage.get(State, state_id).to_dict()), 200
