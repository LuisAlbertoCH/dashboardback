from flask import jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
import json

def json_handler(obj):
    """Manejador para la serialización JSON que maneja ObjectId."""
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

######################################################

# TAREAS

def create_tarea(mongo):
    data = request.json
    Nombre = data.get('Nombre')
    Descripcion = data.get('Descripcion')
    ProyectoId = data.get('ProyectoId')

    if Nombre and ProyectoId:
        tarea = {
            'Nombre': Nombre,
            'Descripcion': Descripcion,
            'ProyectoId': ObjectId(ProyectoId),
        }
        mongo.db.tareas.insert_one(tarea)
        return jsonify(tarea), 201
    else:
        return not_found()

def get_tareas(mongo):
    tareas = mongo.db.tareas.find()
    return Response(json_util.dumps(tareas), mimetype="application/json")

def get_tarea(id, mongo):
    tarea = mongo.db.tareas.find_one({'_id': ObjectId(id)})
    return Response(json_util.dumps(tarea), mimetype="application/json")

def update_tarea(id, mongo):
    data = request.json
    mongo.db.tareas.update_one(
        {'_id': ObjectId(id)},
        {'$set': data}
    )
    return jsonify({'message': f'Tarea {id} actualizada correctamente'}), 200

def delete_tarea(id, mongo):
    mongo.db.tareas.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': f'Tarea {id} eliminada correctamente'}), 200

def not_found():
    return jsonify({'message': 'Recurso no encontrado'}), 404
    
########################################################
def not_found(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response