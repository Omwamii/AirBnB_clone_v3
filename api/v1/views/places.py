#!/usr/bin/python3
""" View to handle search for Place objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.state import State
from models import storage
from os import environ as env


@app_views.route('/cities/<string:city_id>/places',
                 defaults={"place_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/places/<string:place_id>', defaults={"city_id": None},
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def places(place_id, city_id):
    """ operate on Place objects
    """
    if request.method == "POST":
        api_req = request.get_json()
        if api_req is None:
            abort(400, description="Not a JSON")
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
        api_req = request.get_json()
        if api_req is None:
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


@app_views.route("/places_search", methods=['POST'], strict_slashes=False)
def search_places():
    """ retrieves all places depending on the JSON in the request body
    """
    req_body = request.get_json()
    if req_body is None:  # not valid JSON
        abort(400, description="Not a JSON")
    place_objs = list()
    if len(req_body) == 0:
        # JSON body is empty, retrieve all Place objs
        all_places = storage.all(Place)
        for val in all_places.values():
            place_objs.append(val.to_dict())
    else:
        states = req_body['states']
        cities = req_body['cities']
        if req_body.get('amenities'):
            amenity_obj_ids = req_body['amenities']
        else:
            amenity_obj_ids = []
        if len(states) == 0 and len(cities) == 0:
            # return all Place objects
            all_places = storage.all(Place)
            for val in all_Places.values():
                place_objs.append(val.to_dict())
        else:
            city_objs = list()
            for state in states:
                st_obj = storage.get(State, state)
                if st_obj is None:
                    print(f"State: ({state}) not found")
                    abort(404)
                st_city_objs = st_obj.cities
                for city in st_city_objs:
                    city_objs.append(city)
            for city in cities:
                ct_obj = storage.get(City, city)
                if ct_obj is None:
                    print(f"City: ({city}) not found")
                    abort(404)
                if ct_obj not in city_objs:
                    city_objs.append(ct_obj)
            for city_obj in city_objs:
                for place in city_obj.places:
                    place_objs.append(place)
            if len(amenity_obj_ids) != 0:
                # filter place objects to those with set amenities
                to_filter = list()
                if env.get('HBNB_TYPE_STORAGE') == "db":
                    amenity_objs = list()
                    for amenity_id in amenity_obj_ids:
                        am_obj = storage.get(Amenity, amenity_id)
                        if am_obj is None:
                            print(f"Amenity: ({amenity_id}) not found")
                            abort(404)
                        amenity_objs.append(am_obj)
                    for index, pl_obj in enumerate(place_objs):
                        for amenity in amenity_objs:
                            if amenity not in pl_obj.amenities:
                                to_filter.append(index)
                else:  # FileStorage
                    for index, pl_obj in enumerate(place_objs):
                        for amenity in amenity_obj_ids:
                            if amenity not in pl_obj.amenity_ids:
                                to_filter.append(index)
                # trav in rev to delete objs without affecting their positions
                for ind in reversed(to_filter):
                    # filter place objs without the amenities
                    place_objs.pop(ind)
            place_objs_info = list()
            for pl_obj in place_objs:
                place_objs_info.append(pl_obj.to_dict())
            return jsonify(place_objs_info)
