#!/usr/bin/python3
"""assign URLs in our app to functions"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.user import User


@app_views.route("/users", methods=['POST'], strict_slashes=False)
def postUser():
    """post an user"""
    Rdict = request.get_json(force=True, silent=True)
    if Rdict is not None:
        if not Rdict.get('email'):
            return abort(400, "Missing email")
        if not Rdict.get('password'):
            return abort(400, "Missing password")
        obj = User(**Rdict)
        storage.new(obj)
        storage.save()
        return obj.to_dict(), 201
    else:
        return abort(400, "Not a JSON")


@app_views.route("/users/<user_id>", methods=['PUT'], strict_slashes=False)
def putUser(user_id):
    """updates an user"""
    ignore = ["id", "email", "created_at", "updated_at"]
    flag = storage.get(User, user_id)
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


@app_views.route("/users", methods=['GET'], strict_slashes=False)
def users():
    """return a json object"""
    db = storage.all(User)
    lista = []
    for key in db:
        lista.append(db[key].to_dict())
    return jsonify(lista)


@app_views.route("/users/<user_id>", methods=['GET'], strict_slashes=False)
def user(user_id):
    """
    endpoint that retrieves the number of each objects by type
    """
    try:
        return storage.get(User, user_id).to_dict()
    except Exception:
        return abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def rmuser(user_id):
    """
    delete users objects from storage by id
    """
    flag = storage.get(User, user_id)
    if flag:
        storage.delete(flag)
        storage.save()
        return {}, 200
    else:
        return abort(404)
