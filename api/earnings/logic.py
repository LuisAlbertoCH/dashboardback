from flask import jsonify, request, Response
from bson import json_util, ObjectId
import json

# Crear una ganancia
def create_earning(mongo, project_id, total_income, operation_expenses):
    project_id = request.json['project_id']
    total_income = request.json['total_income']
    operation_expenses = request.json['operation_expenses']
    
    net_income = total_income - operation_expenses
    earning = {'project_id': ObjectId(project_id), 'total_income': total_income, 'operation_expenses': operation_expenses, 'net_income': net_income}
    mongo.db.earnings.insert_one(earning)
    
    response = jsonify({'project_id': project_id, 'total_income': total_income, 'operation_expenses': operation_expenses, 'net_income': net_income})
    response.status_code = 201
    return response

# Obtener todas las ganancias
def get_earnings(mongo):
    earnings = mongo.db.earnings.find()
    response = json_util.dumps(earnings)
    return Response(response, mimetype="application/json")

# Obtener una ganancia por ID
def get_earning(id, mongo):
    earning = mongo.db.earnings.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(earning)
    return Response(response, mimetype="application/json")

# Actualizar una ganancia por ID
def update_earning(id, mongo, total_income, operation_expenses):
    total_income = request.json['total_income']
    operation_expenses = request.json['operation_expenses']
    net_income = total_income - operation_expenses
    
    mongo.db.earnings.update_one({'_id': ObjectId(id)}, {'$set': {'total_income': total_income, 'operation_expenses': operation_expenses, 'net_income': net_income}})
    response = jsonify({'message': 'Earning ' + id + ' Updated Successfully'})
    response.status_code = 200
    return response

# Eliminar una ganancia por ID
def delete_earning(id, mongo):
    mongo.db.earnings.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Earning ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response
