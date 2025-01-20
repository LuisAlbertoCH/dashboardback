from flask import request
from .logic import create_note, get_notes_by_talent, update_note, delete_note

def setup_notes_routes(app, mongo):
    @app.route('/notes', methods=['POST'])
    def create_note_route():
        data = request.json
        talent_id = data.get('talent_id')
        content = data.get('content')
        return create_note(mongo, talent_id, content)

    @app.route('/notes/<talent_id>', methods=['GET'])
    def get_notes_route(talent_id):
        return get_notes_by_talent(mongo, talent_id)

    @app.route('/notes/<id>', methods=['PUT'])
    def update_note_route(id):
        data = request.json
        content = data.get('content')
        return update_note(id, mongo, content)

    @app.route('/notes/<id>', methods=['DELETE'])
    def delete_note_route(id):
        return delete_note(id, mongo)
