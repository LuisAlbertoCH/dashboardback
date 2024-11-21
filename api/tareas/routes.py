from flask import request
from .logic import (create_tarea, get_tareas, get_tarea, update_tarea, delete_tarea)

# Configurar las rutas para la gestión de empleados
def setup_tareas_routes(app, mongo):
    # Tareas
    @app.route('/tareas', methods=['POST'])
    def create_tarea_route():
        return create_tarea(mongo)

    @app.route('/tareas', methods=['GET'])
    def get_tareas_route():
        return get_tareas(mongo)

    @app.route('/tareas/<id>', methods=['GET'])
    def get_tarea_route(id):
        return get_tarea(id, mongo)

    @app.route('/tareas/<id>', methods=['PUT'])
    def update_tarea_route(id):
        return update_tarea(id, mongo)

    @app.route('/tareas/<id>', methods=['DELETE'])
    def delete_tarea_route(id):
        return delete_tarea(id, mongo)