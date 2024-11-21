from flask import jsonify, request
from werkzeug.security import check_password_hash

#LOGIN

# Función para manejar el proceso de inicio de sesión de los usuarios
def login(mongo, user, password):
    # Obtiene el nombre de usuario y la contraseña de la solicitud JSON
    user = request.json.get('user')
    password = request.json.get('password')

    # Verifica que tanto el usuario como la contraseña hayan sido proporcionados
    if not user or not password:
        # Si falta alguno, devuelve un error
        return jsonify({"error": "Falta usuario o contraseña"}), 400

    # Busca el usuario en la base de datos por el nombre de usuario proporcionado
    usuario_db = mongo.db.usuario.find_one({'user': user})

    # Si encuentra un usuario y la contraseña proporcionada coincide con la contraseña hash almacenada
    if usuario_db and check_password_hash(usuario_db['password'], password):
        # Devuelve un mensaje de éxito y el código de estado HTTP 200
        return jsonify({"message": "Inicio de sesión exitoso"}), 200
    else:
        # Si las credenciales son incorrectas, devuelve un error
        return jsonify({"error": "Credenciales incorrectas"}), 401
