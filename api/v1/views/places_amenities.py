#!/usr/bin/python3
""" View to handle all Amenities linked to Place objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.place import Place
from models.amenity import Amenity
from models.place import Place
from models import storage
from os import environ as env


@app_views.route('/places/<string:place_id>/amenities',
                 defaults={"amenity_id": None},
                 methods=['GET'], strict_slashes=False)
@app_views.route('places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST', 'DELETE'], strict_slashes=False)
def places_amenities(amenity_id, place_id):
    """ operate on linked amenities to Place objects
    """
    if request.method == "POST":
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if env.get('HBNB_TYPE_STORAGE') == "db":
            if amenity in place.amenities:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenities.append(amenity)
        else:
            if amenity.id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            else:
                place.amenity_ids.append(amenity.id)
        storage.save()
        return jsonify(amenity.to_dict()), 201

    if request.method == "GET":
        # retrieve Place object with id
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        linked_amenities = list()
        if env.get('HBNB_TYPE_STORAGE') == "db":
            print("db_storage checked")
            amenities = place.amenities  # use the rlship in db
            for amenity in amenities:
                linked_amenities.append(amenity.to_dict())
        else:
            print("file_storage checked")
            amenities = place.amenity_ids  # file storage
            for amenity in amenites:
                # get the Amenity with the id in list
                amen_obj = storage.get(Amenity, amenity)
                linked_amenities.append(amen_obj.to_dict())
        return jsonify(linked_amenities)

    if request.method == "DELETE":
        # try get the Place object with specific id
        place = storage.get(Place, place_id)
        if place is None:
            abort(404)
        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)
        if env.get('HBNB_TYPE_STORAGE') == "db":
            if amenity not in place.amenities:
                abort(404)  # amenity not linked to place
        else:
            if amenity.id not in place.amenity_ids:
                abort(404)
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
