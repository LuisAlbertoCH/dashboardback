from flask import jsonify, request, Response
from bson import json_util, ObjectId
import json

# Crear un registro de impuestos
def create_tax(mongo, project_id, federal_entity, sat, imss):
    project_id = request.json['project_id']
    federal_entity = request.json['federal_entity']
    sat = request.json['sat']
    imss = request.json['imss']
    
    # Calcula la ganancia después de impuestos
    total_deductions = sat + imss
    net_income = max(0, 1000 - total_deductions)  # Ejemplo, parte fija, modificar según cálculo real

    tax_record = {
        'project_id': ObjectId(project_id),
        'federal_entity': federal_entity,
        'sat': sat,
        'imss': imss,
        'net_income': net_income
    }
    mongo.db.taxes.insert_one(tax_record)

    response = jsonify(tax_record)
    response.status_code = 201
    return response

# Obtener todos los registros de impuestos
def get_taxes(mongo):
    taxes = mongo.db.taxes.find()
    response = json_util.dumps(taxes)
    return Response(response, mimetype="application/json")

# Obtener un registro de impuestos por ID
def get_tax(id, mongo):
    tax_record = mongo.db.taxes.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(tax_record)
    return Response(response, mimetype="application/json")

# Actualizar un registro de impuestos por ID
def update_tax(id, mongo, federal_entity, sat, imss):
    federal_entity = request.json['federal_entity']
    sat = request.json['sat']
    imss = request.json['imss']
    
    total_deductions = sat + imss
    net_income = max(0, 1000 - total_deductions)  # Ejemplo de cálculo

    mongo.db.taxes.update_one(
        {'_id': ObjectId(id)}, 
        {'$set': {
            'federal_entity': federal_entity, 
            'sat': sat, 
            'imss': imss, 
            'net_income': net_income
        }}
    )

    response = jsonify({'message': 'Tax ' + id + ' Updated Successfully'})
    response.status_code = 200
    return response

# Eliminar un registro de impuestos por ID
def delete_tax(id, mongo):
    mongo.db.taxes.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Tax ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response
