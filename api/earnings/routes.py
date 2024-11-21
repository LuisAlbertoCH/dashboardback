from flask import request
from .logic import (create_earning, get_earnings, get_earning, update_earning, delete_earning)

def setup_earnings_routes(app, mongo):
    @app.route('/earnings', methods=['POST'])
    def create_earning_route():
        project_id = request.json['project_id']
        total_income = request.json['total_income']
        operation_expenses = request.json['operation_expenses']
        return create_earning(mongo, project_id, total_income, operation_expenses)

    @app.route('/earnings', methods=['GET'])
    def get_earnings_route():
        return get_earnings(mongo)

    @app.route('/earnings/<id>', methods=['GET'])
    def get_earning_route(id):
        return get_earning(id, mongo)

    @app.route('/earnings/<id>', methods=['PUT'])
    def update_earning_route(id):
        total_income = request.json['total_income']
        operation_expenses = request.json['operation_expenses']
        return update_earning(id, mongo, total_income, operation_expenses)

    @app.route('/earnings/<id>', methods=['DELETE'])
    def delete_earning_route(id):
        return delete_earning(id, mongo)
