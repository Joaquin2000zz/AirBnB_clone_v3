#!/usr/bin/python3
"""assign URLs in our app to functions"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.state import State


@app_views.route("/states", methods=['POST'], strict_slashes=False)
def postState():
    """post a state"""
    try:
        Rdict = request.get_json()
        if not Rdict.get('name'):
            return abort(400, "Missing name")
        obj = State(**Rdict)
        storage.new(obj)
        storage.save()
        return obj.to_dict(), 201
    except Exception:
        return abort(400, "Not a JSON")


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def putState(state_id):
    """updates a state"""
    ignore = ["id", "created_at", "updated_at"]
    flag = storage.get(State, state_id)
    if not flag:
        return abort(404)
    try:
        Rdict = request.get_json()
        for key, value in Rdict.items():
            if key not in ignore:
                setattr(flag, key, value)
        storage.save()
        return flag.to_dict(), 200
    except Exception:
        abort(400, "Not a JSON")


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def states():
    """return a json object"""
    db = storage.all(State)
    lista = []
    for key in db:
        lista.append(db[key].to_dict())
    return jsonify(lista)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def state(state_id):
    """
    endpoint that retrieves the number of each objects by type
    """
    key = 'State.' + str(state_id)
    try:
        return jsonify(storage.all()[key].to_dict())
    except Exception:
        return abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def rmstate(state_id):
    """
    delete a state object from storage
    """
    key = "State." + str(state_id)
    try:
        storage.delete(storage.all("State")[key])
        storage.save()
        return {}, 200
    except Exception:
        return abort(404)
