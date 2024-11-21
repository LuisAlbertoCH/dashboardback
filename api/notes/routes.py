from flask import request
from .logic import (create_note, get_notes, get_note, update_note, delete_note)

def setup_notes_routes(app, mongo):
    @app.route('/notes', methods=['POST'])
    def create_note_route():
        data = request.json  # Obtener el cuerpo de la solicitud
        talent_id = data.get('talent_id')  # Extraer talent_id
        content = data.get('content')  # Extraer contenido
        return create_note(mongo, talent_id, content)

    @app.route('/notes', methods=['GET'])
    def get_notes_route():
        return get_notes(mongo)

    @app.route('/notes/<id>', methods=['GET'])
    def get_note_route(id):
        return get_note(id, mongo)

    @app.route('/notes/<id>', methods=['PUT'])
    def update_note_route(id):
        data = request.json  # Obtener el cuerpo de la solicitud
        content = data.get('content')  # Extraer contenido actualizado
        return update_note(id, mongo, content)

    @app.route('/notes/<id>', methods=['DELETE'])
    def delete_note_route(id):
        return delete_note(id, mongo)
