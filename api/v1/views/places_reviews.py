#!/usr/bin/python3
"""assign URLs in our app to functions"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("/places/<place_id>/reviews",
                 methods=['POST'], strict_slashes=False)
def postReview(place_id):
    """post reviews"""
    if storage.get(Place, place_id) is None:
        abort(404)
    Rdict = request.get_json(force=True, silent=True)
    if Rdict is not None:
        if not Rdict.get('text'):
            return abort(400, "Missing text")
        if not Rdict.get('user_id'):
            return abort(400, "Missing user_id")
        if storage.get(User, Rdict.get('user_id')) is None:
            abort(404)
        Rdict['place_id'] = place_id
        obj = Review(**Rdict)
        storage.new(obj)
        storage.save()
        return obj.to_dict(), 201
    else:
        return abort(400, "Not a JSON")


@app_views.route("/reviews/<review_id>", methods=['PUT'], strict_slashes=False)
def putReview(review_id):
    """updates a review"""
    ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
    flag = storage.get(Review, review_id)
    if not flag:
        return abort(404)
    Rdict = request.get_json(force=True, silent=True)
    if Rdict is not None:
        for key, value in Rdict.items():
            if key not in ignore:
                setattr(flag, key, value)
        storage.save()
        return flag.to_dict(), 200
    else:
        abort(400, "Not a JSON")


@app_views.route("places/<place_id>/reviews",
                 methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """return a json object"""
    flag = storage.get(Place, place_id)
    if flag is None:
        abort(404)
    db = storage.all(Review)
    lista = []
    for key in db:
        if db[key].to_dict().get('place_id') == place_id:
            lista.append(db[key].to_dict())
    return jsonify(lista)


@app_views.route("/reviews/<review_id>",
                 methods=['GET'], strict_slashes=False)
def review(review_id):
    """
    endpoint that retrieves the number of each objects by type
    """
    try:
        return storage.get(Review, review_id).to_dict()
    except Exception:
        return abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'],
                 strict_slashes=False)
def rmreview(review_id):
    """
    delete review objects from storage by id
    """
    flag = storage.get(Review, review_id)
    if flag:
        storage.delete(flag)
        storage.save()
        return {}, 200
    else:
        return abort(404)
