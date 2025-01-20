from flask import request, jsonify
from .logic import get_sheet_data, get_workspace_sheets

def setup_smartsheet_routes(app):
    """
    Configura las rutas para la integración con Smartsheet.
    """

    @app.route('/smartsheet/<sheet_id>', methods=['GET'])
    def get_smartsheet_data(sheet_id):
        """
        Ruta para obtener datos de una hoja específica en Smartsheet.
        """
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token de autorización no proporcionado"}), 400

        # Llama a la lógica para obtener los datos de la hoja
        return get_sheet_data(token, sheet_id)
    
    @app.route('/smartsheet/workspace/<workspace_id>', methods=['GET'])
    def get_workspace_data(workspace_id):
        """
        Ruta para obtener las hojas de un espacio de trabajo en Smartsheet.
        """
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error": "Token de autorización no proporcionado"}), 400

        return get_workspace_sheets(token, workspace_id)
