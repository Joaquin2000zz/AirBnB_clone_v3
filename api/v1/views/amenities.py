#!/usr/bin/python3
"""assign URLs in our app to functions"""


from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['POST'], strict_slashes=False)
def postAmenity():
    """post a amenity"""
    try:
        Rdict = request.get_json()
        if not Rdict.get('name'):
            return abort(400, "Missing name")
        obj = Amenity(**Rdict)
        storage.new(obj)
        storage.save()
        return obj.to_dict(), 201
    except Exception:
        return abort(400, "Not a JSON")


r = "/amenities/<amenity_id>"


@app_views.route(r, methods=['PUT'], strict_slashes=False)
def putAmenity(amenity_id):
    """updates a amenity"""
    ignore = ["id", "created_at", "updated_at"]
    flag = storage.get(Amenity, amenity_id)
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


@app_views.route("/amenities", methods=['GET'], strict_slashes=False)
def amenities():
    """return a json object"""
    db = storage.all(Amenity)
    lista = []
    for key in db:
        lista.append(db[key].to_dict())
    return jsonify(lista)


r = "/amenities/<amenity_id>"


@app_views.route(r, methods=['GET'], strict_slashes=False)
def amenity(amenity_id):
    """
    endpoint that retrieves the number of each objects by type
    """
    key = 'Amenity.' + str(amenity_id)
    try:
        return jsonify(storage.all()[key].to_dict())
    except Exception:
        return abort(404)


r = "/amenities/<amenity_id>"


@app_views.route(r, methods=['DELETE'],
                 strict_slashes=False)
def rmamenity(amenity_id):
    """
    delete a amenity object from storage
    """
    key = "Amenity." + str(amenity_id)
    try:
        storage.delete(storage.all("Amenity")[key])
        storage.save()
        return {}, 200
    except Exception:
        return abort(404)
