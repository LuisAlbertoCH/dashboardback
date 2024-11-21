from .logic import create_proyecto, get_proyectos, get_proyecto, update_proyecto, delete_proyecto

# Configurar las rutas para la gestión de proyectos
def setup_proyectos_routes(app, mongo):
    # Crear un nuevo proyecto
    @app.route('/proyectos', methods=['POST'])
    def create_proyecto_route():
        return create_proyecto(mongo)

    # Obtener todos los proyectos
    @app.route('/proyectos', methods=['GET'])
    def get_proyectos_route():
        return get_proyectos(mongo)

    # Obtener un proyecto por ID
    @app.route('/proyectos/<id>', methods=['GET'])
    def get_proyecto_route(id):
        return get_proyecto(id, mongo)

    # Actualizar un proyecto por ID
    @app.route('/proyectos/<id>', methods=['PUT'])
    def update_proyecto_route(id):
        return update_proyecto(id, mongo)

    # Eliminar un proyecto por ID
    @app.route('/proyectos/<id>', methods=['DELETE'])
    def delete_proyecto_route(id):
        return delete_proyecto(id, mongo)
