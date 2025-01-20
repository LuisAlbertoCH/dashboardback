from flask import request, jsonify
from .logic import (create_talento, get_talentos, get_talento, update_talento, delete_talento,agregar_indicador, obtener_indicadores, calcular_evaluacion, update_talent_indicator)

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
    
    @app.route('/talentos/<talent_id>/indicadores', methods=['POST'])
    def agregar_indicador_route(talent_id):
        data = request.json
        valor = data.get('valor')
        descripcion = data.get('descripcion', '')
        if valor is None:
            return jsonify({'error': 'El campo "valor" es obligatorio'}), 400
        return agregar_indicador(mongo, talent_id, valor, descripcion)

    @app.route('/talentos/<talent_id>/indicadores', methods=['GET'])
    def obtener_indicadores_route(talent_id):
        return obtener_indicadores(mongo, talent_id)

    @app.route('/talentos/<talent_id>/evaluacion', methods=['GET'])
    def calcular_evaluacion_route(talent_id):
        return calcular_evaluacion(mongo, talent_id)
    
    @app.route('/talentos/<talent_id>/indicadores/<indicator_id>', methods=['PUT'])
    def update_talent_indicator_route(talent_id, indicator_id):
        value = request.json.get('valor')  # Obtener el valor del indicador del cuerpo de la solicitud
        return update_talent_indicator(mongo, talent_id, indicator_id, value)

