from flask import jsonify, request, Response
from bson import json_util, ObjectId
import json

# Crear un indicador
def create_indicator(mongo, talent_id, task_id, status, delivery_time):
    talent_id = request.json['talent_id']
    task_id = request.json['task_id']
    status = request.json['status']
    delivery_time = request.json['delivery_time']
    
    indicator = {'talent_id': ObjectId(talent_id), 'task_id': ObjectId(task_id), 'status': status, 'delivery_time': delivery_time}
    mongo.db.indicators.insert_one(indicator)
    
    response = jsonify({'talent_id': talent_id, 'task_id': task_id, 'status': status, 'delivery_time': delivery_time})
    response.status_code = 201
    return response

# Obtener todos los indicadores
def get_indicators(mongo):
    indicators = mongo.db.indicators.find()
    response = json_util.dumps(indicators)
    return Response(response, mimetype="application/json")

# Obtener un indicador por ID
def get_indicator(id, mongo):
    indicator = mongo.db.indicators.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(indicator)
    return Response(response, mimetype="application/json")

# Actualizar un indicador por ID
def update_indicator(id, mongo, status, delivery_time):
    status = request.json['status']
    delivery_time = request.json['delivery_time']
    
    mongo.db.indicators.update_one({'_id': ObjectId(id)}, {'$set': {'status': status, 'delivery_time': delivery_time}})
    response = jsonify({'message': 'Indicator ' + id + ' Updated Successfully'})
    response.status_code = 200
    return response

# Eliminar un indicador por ID
def delete_indicator(id, mongo):
    mongo.db.indicators.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Indicator ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response
