from flask import jsonify, request, Response
from bson import json_util, ObjectId
import json

# Crear una nota
def create_note(mongo, talent_id, content):
    try:
        # Crear la nota con ObjectId convertido a cadena para la respuesta
        note = {
            'talent_id': ObjectId(talent_id),  # Usamos ObjectId aquí para MongoDB
            'content': content
        }
        mongo.db.notes.insert_one(note)
        
        # Convertir talent_id a cadena para la respuesta JSON
        note['_id'] = str(note['_id']) if '_id' in note else None
        note['talent_id'] = str(note['talent_id'])

        return jsonify({'message': 'Nota creada exitosamente', 'note': note}), 201
    except Exception as e:
        return jsonify({'error': 'Error al crear la nota', 'details': str(e)}), 500

# Obtener todas las notas
def get_notes(mongo):
    notes = mongo.db.notes.find()
    response = json_util.dumps(notes)
    return Response(response, mimetype="application/json")

# Obtener una nota por ID
def get_note(id, mongo):
    note = mongo.db.notes.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(note)
    return Response(response, mimetype="application/json")

# Actualizar una nota por ID
def update_note(id, mongo, content):
    content = request.json['content']
    
    mongo.db.notes.update_one({'_id': ObjectId(id)}, {'$set': {'content': content}})
    response = jsonify({'message': 'Note ' + id + ' Updated Successfully'})
    response.status_code = 200
    return response

# Eliminar una nota por ID
def delete_note(id, mongo):
    mongo.db.notes.delete_one({'_id': ObjectId(id)})
    response = jsonify({'message': 'Note ' + id + ' Deleted Successfully'})
    response.status_code = 200
    return response
