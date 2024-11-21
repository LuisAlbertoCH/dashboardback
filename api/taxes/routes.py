from flask import request
from .logic import (create_tax, get_taxes, get_tax, update_tax, delete_tax)

def setup_taxes_routes(app, mongo):
    @app.route('/taxes', methods=['POST'])
    def create_tax_route():
        project_id = request.json['project_id']
        federal_entity = request.json['federal_entity']
        sat = request.json['sat']
        imss = request.json['imss']
        return create_tax(mongo, project_id, federal_entity, sat, imss)

    @app.route('/taxes', methods=['GET'])
    def get_taxes_route():
        return get_taxes(mongo)

    @app.route('/taxes/<id>', methods=['GET'])
    def get_tax_route(id):
        return get_tax(id, mongo)

    @app.route('/taxes/<id>', methods=['PUT'])
    def update_tax_route(id):
        federal_entity = request.json['federal_entity']
        sat = request.json['sat']
        imss = request.json['imss']
        return update_tax(id, mongo, federal_entity, sat, imss)

    @app.route('/taxes/<id>', methods=['DELETE'])
    def delete_tax_route(id):
        return delete_tax(id, mongo)
