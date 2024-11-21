from flask import jsonify, request, Response
from bson import json_util, ObjectId
import json

# Crear un plan de trabajo
def create_workplan(mongo, project_id, delivery_date):
    project_id = request.json['project_id']
    delivery_date = request.json['delivery_date']
    
    workplan = {'project_id': ObjectId(project_id), 'delivery_date': delivery_date}
    mongo.db.workplan.insert_one(workplan)
    
    response = jsonify({'project_id': project_id, 'delivery_date': delivery_date})
    response.status_code = 201
    return response

# Obtener todos los planes de trabajo
def get_workplans(mongo):
    workplans = mongo.db.workplan.find()
    response = json_util.dumps(workplans)
    return Response(response, mimetype="application/json")

# Obtener un plan de trabajo por ID
def get_workplan(id, mongo):
    workplan = mongo.db.workplan.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(workplan)
    return Response(response, mimetype="application/json")

# Actualizar un plan de trabajo por ID
def update_workplan(id, mongo, delivery_date):
    delivery_date = request.json['delivery_date']
    
    mongo.db.workplan.update_one({'_id': ObjectId(id)}, {'$set': {'delivery_date': delivery_date}})
    response = jsonify({'message': 'Work Plan ' + id + ' Updated Successfully'})
    response.status_code = 200
    return response

# Eliminar un plan de trabajo por ID
def delete_workplan(id, mongo):
    mongo.db.workplan.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Work Plan ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response
