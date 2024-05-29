#!/usr/bin/python3
""" City objects that handles all default RestFul API actions """
from models.city import City
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'],
        strict_slashes=False)
def cities(state_id):
    """Status of API"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities]), 200


@app_views.route(
        '/cities/<city_id>', methods=['GET'],
        strict_slashes=False)
def city_id(city_id):
    """Retrieves the number of each objects by type"""
    city = storage.get(City, city_id)
    if not city:
        return abort(404)
    return jsonify(city.to_dict()), 200


@app_views.route(
        '/cities/<city_id>', methods=['DELETE'],
        strict_slashes=False)
def delete_city(city_id):
    """Delete city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'],
        strict_slashes=False)
def post_city(state_id):
    """Create a new city"""
    data = request.get_json()

    if not storage.get(State, state_id):
        abort(404)
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")

    instance = City(**data)
    setattr(instance, 'state_id', state_id)
    storage.new(instance)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route(
        '/cities/<city_id>', methods=['PUT'],
        strict_slashes=False)
def put_city(city_id):
    """Update a city"""
    city = storage.get(City, city_id)
    data = request.get_json()

    if not city:
        abort(404)

    if not data:
        abort(400, "Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
