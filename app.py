from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_cors import CORS
import logging
import requests

def json_handler(obj):
    """Manejador para la serialización JSON que maneja ObjectId."""
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

# Crear una instancia de la aplicación Flask
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'application/json'

# Aplica CORS a la aplicación para permitir solicitudes desde localhost:5001
CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST", "PUT", "DELETE"])

#Aplica CORS a la aplicación para permitir solicitudes desde otros dominios
cors = CORS(app) 

#Congifuración de la URI que se conecta al servidor de MongoDB (Cibercom)
app.config['MONGO_URI'] = 'mongodb+srv://lcancelah:IliB1ztGrBd52uoz@cluster0.krqlf.mongodb.net/dashboardbackend?retryWrites=true&w=majority&appName=Cluster0'
#mongodb+srv://cibercom:cibercom123@cluster0.7gjmcsf.mongodb.net/dashboardbackend?retryWrites=true&w=majority
#'mongodb://localhost/backdashboard'

#Se crea una instancia de PyMongo para interactuar con MongoDB
mongo = PyMongo(app)

# Configura el nivel de registro para el sistema de registro (logging)
logging.basicConfig(level=logging.DEBUG)

SMARTSHEET_API_URL = "https://api.smartsheet.com/2.0"
SMARTSHEET_TOKEN = "2Cc87jOA2pZBUfPdKy1qwppXVqgVMbqsk8ngF"

#Aqui se importan las funciones de configuración de rutas de otros módulos que se encuentran en el apartado api de la raíz
# Estas funciones definen las rutas y cómo se manejan las solicitudes HTTP
from api.login.routes import setup_login_routes
from api.usuario.routes import setup_usuario_routes
from api.talentos.routes import setup_talentos_routes
from api.proyectos.routes import setup_proyectos_routes
from api.tareas.routes import setup_tareas_routes
from api.notes.routes import setup_notes_routes
from api.indicators.routes import setup_indicators_routes
from api.xml.routes import setup_xml_route
from api.earnings.routes import setup_earnings_routes
from api.taxes.routes import setup_taxes_routes
from api.visits.routes import setup_visits_routes
from api.workplan.routes import setup_workplan_routes
from api.smartsheet.routes import setup_smartsheet_routes

#Configurar las rutas llamando a esas funciones de configuración de rutas definidas en otros módulos
setup_login_routes(app, mongo)
setup_usuario_routes(app, mongo)
setup_talentos_routes(app, mongo)
setup_proyectos_routes(app, mongo)
setup_tareas_routes(app, mongo)
setup_notes_routes(app, mongo)
setup_indicators_routes(app, mongo)
setup_xml_route(app, mongo)
setup_earnings_routes(app, mongo)
setup_taxes_routes(app, mongo)
setup_visits_routes(app, mongo)
setup_workplan_routes(app, mongo)
setup_smartsheet_routes(app)

########################################################

#Esta función maneja recursos no encontrados en alguna petición HTTP realizadas a la API REST
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response

#Ejecuta la aplicación en modo depuración y se asigna el puerto de manera manual
if __name__ == "__main__":
    app.run(debug=True, port=5000)
