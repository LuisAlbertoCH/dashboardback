from flask import request
from .logic import (login)

# Esta función configura las rutas relacionadas con las operaciones de inicio de sesión.
def setup_login_routes(app, mongo):
    # Define la ruta '/login' que acepta solicitudes POST para iniciar sesión.
    @app.route('/login', methods=['POST'])
    def login_route():
        # Obtiene el nombre de usuario y la contraseña de los datos de la solicitud JSON.
        user = request.json.get('user')
        password = request.json.get('password')
        
        # Llama a la función de inicio de sesión definida en 'logic.py' con los datos del usuario.
        # Pasa la instancia de la base de datos MongoDB, el nombre de usuario y la contraseña para la autenticación.
        return login(mongo, user, password)
