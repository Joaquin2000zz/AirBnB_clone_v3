#!/usr/bin/python3
"""assign URLs in our app to functions"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place
from models.user import User


r = "/cities/<city_id>/places"


@app_views.route(r, methods=['POST'], strict_slashes=False)
def postPlace(city_id):
    """post a place"""
    if storage.get(City, city_id) is None:
        return abort(404)
    Rdict = request.get_json(force=True, silent=True)
    if Rdict is not None:
        if Rdict.get('user_id') is None:
            return abort(400, "Missing user_id")
        if storage.get(User, Rdict.get("user_id")) is None:
            return abort(404)
        if Rdict.get("name") is None:
            return abort(400, "Missing name")
        if storage.get(User, Rdict.get("user_id")) is None:
            abort(404)
        Rdict["city_id"] = city_id
        obj = Place(**Rdict)
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201
    else:
        return abort(400, "Not a JSON")


@app_views.route("/places/<place_id>", methods=['PUT'], strict_slashes=False)
def putPlace(place_id):
    """updates a state"""
    ignore = ["id", "created_at", "updated_at"]
    flag = storage.get(Place, place_id)
    if not flag:
        return abort(404)
    Rdict = request.get_json(force=True, silent=True)
    if Rdict is not None:
        for key, value in Rdict.items():
            if key not in ignore:
                setattr(flag, key, value)
        storage.save()
        return jsonify(flag.to_dict()), 200
    else:
        abort(400, "Not a JSON")


r = "/cities/<city_id>/places"


@app_views.route(r, methods=['GET'], strict_slashes=False)
def places(city_id):
    """return a json object"""
    if storage.get(City, str(city_id)) is None:
        return abort(404)
    db = storage.all(Place)
    lista = []
    for key in db:
        if db[key].city_id == str(city_id):
            lista.append(db[key].to_dict())
    return jsonify(lista)


@app_views.route("/places/<place_id>", methods=['GET'], strict_slashes=False)
def place(place_id):
    """
    endpoint that retrieves the number of each objects by type
    """
    key = 'Place.' + str(place_id)
    try:
        return jsonify(storage.all()[key].to_dict())
    except Exception:
        return abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def rmplace(place_id):
    """
    delete a state object from storage
    """
    key = "Place." + str(place_id)
    try:
        storage.all(Place)[key].delete()
        storage.save()
        return {}, 200
    except Exception:
        return abort(404)
