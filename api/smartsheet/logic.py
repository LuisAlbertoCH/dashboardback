import requests
from flask import jsonify

# URL base de Smartsheet API
BASE_URL = "https://api.smartsheet.com/2.0"
API_KEY = '2Cc87jOA2pZBUfPdKy1qwppXVqgVMbqsk8ngF'

def get_sheet_data(token, sheet_id):
    """
    Obtiene los datos de una hoja específica de Smartsheet.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}/sheets/{sheet_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Genera excepción para códigos HTTP de error
        return response.json()  # Retorna los datos de la hoja en formato JSON
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al obtener datos de Smartsheet", "details": str(e)}), 500

def get_workspace_sheets(token, workspace_id):
    """
    Obtiene las hojas dentro de un espacio de trabajo específico en Smartsheet.
    """
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"{BASE_URL}/workspaces/{workspace_id}"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Error al obtener datos del espacio de trabajo", "details": str(e)}), 500
