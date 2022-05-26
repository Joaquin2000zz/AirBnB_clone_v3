#!/usr/bin/python3
"""assign URLs in our app to functions"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities",
                 methods=['POST'], strict_slashes=False)
def postCity(state_id):
    """post an city"""
    if storage.get(State, state_id) is None:
        abort(404)
    Rdict = request.get_json(force=True, silent=True)
    if Rdict is not None:
        if not Rdict.get('name'):
            return abort(400, "Missing name")
        Rdict['state_id'] = state_id
        obj = City(**Rdict)
        storage.new(obj)
        storage.save()
        return obj.to_dict(), 201
    else:
        return abort(400, "Not a JSON")


@app_views.route("/cities/<city_id>", methods=['PUT'], strict_slashes=False)
def putCity(city_id):
    """updates a city"""
    ignore = ["id", "state_id", "created_at", "updated_at"]
    flag = storage.get(City, city_id)
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


@app_views.route("states/<state_id>/cities",
                 methods=['GET'], strict_slashes=False)
def cities(state_id):
    """return a json object"""
    flag = storage.get(State, state_id)
    if flag is None:
        abort(404)
    db = storage.all(City)
    lista = []
    for key in db:
        if db[key].to_dict().get('state_id') == state_id:
            lista.append(db[key].to_dict())
    return jsonify(lista)


@app_views.route("/cities/<city_id>", methods=['GET'], strict_slashes=False)
def city(city_id):
    """
    endpoint that retrieves the number of each objects by type
    """
    try:
        return storage.get(City, city_id).to_dict()
    except Exception:
        return abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'],
                 strict_slashes=False)
def rmcity(city_id):
    """
    delete city objects from storage by id
    """
    flag = storage.get(City, city_id)
    if flag:
        storage.delete(flag)
        storage.save()
        return {}, 200
    else:
        return abort(404)
