from flask import jsonify, Response
from bson import json_util

# Aumentar el contador de visitas
def increment_visits(mongo):
    mongo.db.visits.update_one({}, {'$inc': {'count': .5}}, upsert=True)
    visit_count = mongo.db.visits.find_one({})
    response = json_util.dumps(visit_count)
    return Response(response, mimetype="application/json")

# Obtener el total de visitas
def get_visits(mongo):
    visit_count = mongo.db.visits.find_one({})
    response = json_util.dumps(visit_count)
    return Response(response, mimetype="application/json")
