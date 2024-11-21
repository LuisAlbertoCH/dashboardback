from flask import request
from .logic import (create_indicator, get_indicators, get_indicator, update_indicator, delete_indicator)

def setup_indicators_routes(app, mongo):
    @app.route('/indicators', methods=['POST'])
    def create_indicator_route():
        talent_id = request.json['talent_id']
        task_id = request.json['task_id']
        status = request.json['status']
        delivery_time = request.json['delivery_time']
        return create_indicator(mongo, talent_id, task_id, status, delivery_time)

    @app.route('/indicators', methods=['GET'])
    def get_indicators_route():
        return get_indicators(mongo)

    @app.route('/indicators/<id>', methods=['GET'])
    def get_indicator_route(id):
        return get_indicator(id, mongo)

    @app.route('/indicators/<id>', methods=['PUT'])
    def update_indicator_route(id):
        status = request.json['status']
        delivery_time = request.json['delivery_time']
        return update_indicator(id, mongo, status, delivery_time)

    @app.route('/indicators/<id>', methods=['DELETE'])
    def delete_indicator_route(id):
        return delete_indicator(id, mongo)
