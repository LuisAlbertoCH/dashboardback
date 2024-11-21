from flask import request
from .logic import (create_usuario, get_usuarios, get_usuario, delete_usuario, update_usuario)

# Esta función configura las rutas para las operaciones CRUD de usuarios
def setup_usuario_routes(app, mongo):
    # Ruta para crear un nuevo usuario
    @app.route('/usuario', methods=['POST'])
    def create_usuario_route():
        # Extrae el nombre de usuario y la contraseña de la solicitud
        user = request.json['user']
        password = request.json['password']
        # Llama a la función de lógica para crear el usuario y devuelve la respuesta
        return create_usuario(mongo, user, password)

    # Ruta para obtener todos los usuarios
    @app.route('/usuarios', methods=['GET'])
    def get_usuarios_route():
        # Llama a la función de lógica para obtener todos los usuarios y devuelve la respuesta
        return get_usuarios(mongo)

    # Ruta para obtener un usuario específico por su ID
    @app.route('/usuario/<id>', methods=['GET'])
    def get_usuario_route(id):
        # Llama a la función de lógica para obtener un usuario por su ID y devuelve la respuesta
        return get_usuario(mongo, id)

    # Ruta para actualizar un usuario específico por su ID
    @app.route('/usuario/<id>', methods=['PUT'])
    def update_usuario_route(id):
        # Extrae el nombre de usuario y la contraseña actualizados de la solicitud
        user = request.json['user']
        password = request.json['password']
        # Llama a la función de lógica para actualizar el usuario y devuelve la respuesta
        return update_usuario(mongo, id, user, password)

    # Ruta para eliminar un usuario específico por su ID
    @app.route('/usuario/<id>', methods=['DELETE'])
    def delete_usuario_route(id):
        # Llama a la función de lógica para eliminar el usuario por su ID y devuelve la respuesta
        return delete_usuario(mongo, id)