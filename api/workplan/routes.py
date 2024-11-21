from flask import request
from .logic import (create_workplan, get_workplans, get_workplan, update_workplan, delete_workplan)

def setup_workplan_routes(app, mongo):
    @app.route('/workplan', methods=['POST'])
    def create_workplan_route():
        project_id = request.json['project_id']
        delivery_date = request.json['delivery_date']
        return create_workplan(mongo, project_id, delivery_date)

    @app.route('/workplan', methods=['GET'])
    def get_workplans_route():
        return get_workplans(mongo)

    @app.route('/workplan/<id>', methods=['GET'])
    def get_workplan_route(id):
        return get_workplan(id, mongo)

    @app.route('/workplan/<id>', methods=['PUT'])
    def update_workplan_route(id):
        delivery_date = request.json['delivery_date']
        return update_workplan(id, mongo, delivery_date)

    @app.route('/workplan/<id>', methods=['DELETE'])
    def delete_workplan_route(id):
        return delete_workplan(id, mongo)
