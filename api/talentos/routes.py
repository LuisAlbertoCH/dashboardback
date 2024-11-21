from flask import request
from .logic import (create_talento, get_talentos, get_talento, update_talento, delete_talento)

# Configurar las rutas para la gestión de empleados
def setup_talentos_routes(app, mongo):
    # Talentos
    @app.route('/talentos', methods=['POST'])
    def create_talento_route():
        return create_talento(mongo)

    @app.route('/talentos', methods=['GET'])
    def get_talentos_route():
        return get_talentos(mongo)

    @app.route('/talentos/<id>', methods=['GET'])
    def get_talento_route(id):
        return get_talento(id, mongo)

    @app.route('/talentos/<id>', methods=['PUT'])
    def update_talento_route(id):
        return update_talento(id, mongo)

    @app.route('/talentos/<id>', methods=['DELETE'])
    def delete_talento_route(id):
        return delete_talento(id, mongo)