#!/usr/bin/python3
""" View to handle all User objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.user import User
from models import storage


@app_views.route('/users', defaults={"user_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/users/<string:user_id>',
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def users(user_id):
    """ operate on User objects
    """
    if request.method == "POST":
        api_req = request.get_json()
        if api_req is None:
            abort(400, description="Not a JSON")
        if 'name' not in api_req:
            abort(400, description="Missing name")
        elif 'email' not in api_req:
            abort(400, description="Missing email")
        elif 'password' not in api_req:
            abort(400, description="Missing password")
        else:
            # create object and return status code 201
            obj = User(**api_req)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201

    if request.method == "GET":
        if user_id is None:
            # return all User objects
            all_users = storage.all(User)
            users = list()
            for val in all_users.values():
                users.append(val.to_dict())
            return jsonify(users)
        else:
            # get user with specific user_id
            obj = storage.get(User, user_id)
            if obj is None:
                abort(404)
            return jsonify(obj.to_dict())
    if request.method == "DELETE":
        # try get the object with specific id
        obj = storage.get(User, user_id)
        # if object doesn't exist raise 404 error
        if obj is None:
            abort(404)
        # if found delete object and return empty dict with status 200
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        # if user_id not linked to any User, raise 404
        obj = storage.get(User, user_id)
        if obj is None:
            abort(404)
        api_req = request.get_json()
        if api_req is None:
            # if not valid json raise 400 with 'Not a JSON'
            abort(400, description="Not a JSON")
        else:
            # update User obj with the key-val pairs
            for key, val in api_req.items():
                if key not in ("id", "created_at", "updated_at", "email"):
                    setattr(obj, key, val)
            storage.save()
            return jsonify(storage.get(User, user_id).to_dict()), 200
