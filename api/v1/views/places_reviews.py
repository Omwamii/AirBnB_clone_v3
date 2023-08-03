#!/usr/bin/python3
""" View to handle all Review objects
"""
from api.v1.views import app_views
from flask import abort
from flask import jsonify
from flask import request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>/reviews',
                 defaults={"review_id": None},
                 methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/reviews/<string:review_id>', defaults={"place_id": None},
                 methods=['GET', 'DELETE', 'PUT'], strict_slashes=False)
def reviews(review_id, place_id):
    """ operate on Review objects
    """
    if request.method == "POST":
        api_req = request.get_json()
        if api_req is None:
            abort(400, description="Not a JSON")
        if 'user_id' not in api_req:
            abort(400, description="Missing user_id")
        if 'text' not in api_req:
            abort(400, description="Missing text")
        else:
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            user = storage.get(User, api_req['user_id'])
            if user is None:
                abort(404)
            api_req['place_id'] = place_id
            obj = Review(**api_req)
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201

    if request.method == "GET":
        if place_id is not None:
            # retrieve Place object with id
            place = storage.get(Place, place_id)
            if place is None:
                abort(404)
            linked_reviews = list()
            reviews = place.reviews
            for review in reviews:
                linked_reviews.append(review.to_dict())
            return jsonify(linked_reviews)
        else:
            review = storage.get(Review, review_id)
            if review is None:
                abort(404)
            return jsonify(review.to_dict())
    if request.method == "DELETE":
        # try get the object with specific id
        review = storage.get(Review, review_id)
        # if review doesn't exist raise 404 error
        if review is None:
            abort(404)
        # if found delete object and return empty dict with status 200
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == "PUT":
        api_req = request.get_json()
        if api_req is None:
            # if not valid json raise 400 with 'Not a JSON'
            abort(400, description="Not a JSON")
        else:
            # if review_id not linked to any review, raise 404
            review = storage.get(Review, review_id)
            if review is None:
                abort(404)
            # update Review obj with the key-val pairs
            for key, val in api_req.items():
                if key not in ("id", "created_at", "updated_at",
                               "place_id", "user_id"):
                    setattr(review, key, val)
            storage.save()
            return jsonify(storage.get(Review, review_id).to_dict()), 200
