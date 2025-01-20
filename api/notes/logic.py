from flask import jsonify, request, Response
from bson import json_util, ObjectId
from bson.errors import InvalidId

# Crear una nota
def create_note(mongo, talent_id, content):
    try:
        if not talent_id or not content:
            return jsonify({'error': 'talent_id y content son obligatorios'}), 400

        note = {
            'talent_id': ObjectId(talent_id),
            'content': content
        }
        mongo.db.notes.insert_one(note)
        note['_id'] = str(note['_id'])
        note['talent_id'] = str(note['talent_id'])

        return jsonify({'message': 'Nota creada exitosamente', 'note': note}), 201
    except InvalidId:
        return jsonify({'error': 'talent_id no es un ObjectId válido'}), 400
    except Exception as e:
        return jsonify({'error': 'Error al crear la nota', 'details': str(e)}), 500

# Obtener notas por talento
def get_notes_by_talent(mongo, talent_id):
    try:
        # Validar si talent_id es un ObjectId válido
        talent_id_obj = ObjectId(talent_id)
        notes = list(mongo.db.notes.find({'talent_id': talent_id_obj}))
        for note in notes:
            note['_id'] = str(note['_id'])
            note['talent_id'] = str(note['talent_id'])

        return jsonify(notes), 200
    except InvalidId:
        return jsonify({'error': 'talent_id no es un ObjectId válido'}), 400
    except Exception as e:
        return jsonify({'error': 'Error al obtener las notas', 'details': str(e)}), 500

# Actualizar una nota por ID
def update_note(id, mongo, content):
    try:
        mongo.db.notes.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'content': content}}
        )
        return jsonify({'message': f'Nota {id} actualizada exitosamente'}), 200
    except InvalidId:
        return jsonify({'error': 'ID de nota no es válido'}), 400
    except Exception as e:
        return jsonify({'error': 'Error al actualizar la nota', 'details': str(e)}), 500

# Eliminar una nota por ID
def delete_note(id, mongo):
    try:
        mongo.db.notes.delete_one({'_id': ObjectId(id)})
        return jsonify({'message': f'Nota {id} eliminada exitosamente'}), 200
    except InvalidId:
        return jsonify({'error': 'ID de nota no es válido'}), 400
    except Exception as e:
        return jsonify({'error': 'Error al eliminar la nota', 'details': str(e)}), 500
