from flask import jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
import json, datetime

def json_handler(obj):
    """Manejador para la serialización JSON que maneja ObjectId."""
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

######################################################

# TALENTOS

# Ruta para crear un talento
def create_talento(mongo):
    try:
        data = request.json
        Nombre = data.get('Nombre')
        ApelPaterno = data.get('ApelPaterno')
        ApelMaterno = data.get('ApelMaterno')
        Email = data.get('Email')
        Fotografia = data.get('Fotografia')

        if Nombre and ApelPaterno and Email:
            talento = {
                'Nombre': Nombre,
                'ApelPaterno': ApelPaterno,
                'ApelMaterno': ApelMaterno,
                'Email': Email,
                'Fotografia': Fotografia,
                'indicadores': [] 
            }
            mongo.db.talentos.insert_one(talento)
            response = jsonify(talento)
            response.status_code = 201
            return response
        else:
            return jsonify({"error": "Faltan datos necesarios"}), 400
    except Exception as e:
        # Captura el error y devuelve una respuesta detallada
        return jsonify({"error": "Talento registrado", "details": str(e)}), 201

# Ruta para obtener todos los talentos
def get_talentos(mongo):
    # Obtener todos los talentos de la base de datos
    talentos = mongo.db.talentos.find()

    # Convertir la respuesta BSON a JSON
    response = json_util.dumps(talentos)
    response = json.loads(response)

    # Formatear la respuesta para incluir _id y convertir en JSON
    talentos_lista = []
    for t in response:
        fn = t.get("Fotografia", '')
        talentos_lista.append({
            '_id': t["_id"]["$oid"],
            'Nombre': t["Nombre"],
            'ApelPaterno': t["ApelPaterno"],
            'ApelMaterno': t["ApelMaterno"],
            'Email': t["Email"],
            'Fotografia': fn,
        })
    talentos_lista = json.dumps(talentos_lista)

    # Devolver la respuesta JSON
    return Response(talentos_lista, mimetype="application/json")

# Ruta para obtener un talento por su ID
def get_talento(id, mongo):
    # Buscar el talento por su ID en la base de datos
    talento = mongo.db.talentos.find_one({'_id': ObjectId(id)})
    # Convertir la respuesta BSON a JSON
    response = json_util.dumps(talento)
    return Response(response, mimetype="application/json")

# Ruta para eliminar un talento por su ID
def delete_talento(id, mongo):
    # Eliminar el talento de la base de datos
    mongo.db.talentos.delete_one({'_id': ObjectId(id)})
    # Verificar si se eliminó correctamente y devolver la respuesta apropiada
    response = jsonify({'message': 'Talento ' + id + ' eliminado correctamente'})
    response.status_code = 200
    return response

# Ruta para actualizar un talento por su ID
def update_talento(id, mongo):
    # Obtener los datos JSON de la solicitud
    Nombre = request.json.get('Nombre')
    ApelPaterno = request.json.get('ApelPaterno')
    ApelMaterno = request.json.get('ApelMaterno')
    Email = request.json.get('Email')
    Fotografia = request.json.get('Fotografia', None)  # Opcional

    # Validar que los campos necesarios tengan datos
    if Nombre and ApelPaterno and Email:
        # Crear el diccionario con los datos actualizados
        talento_actualizado = {
            'Nombre': Nombre,
            'ApelPaterno': ApelPaterno,
            'ApelMaterno': ApelMaterno,
            'Email': Email,
            'Fotografia': Fotografia
        }
        # Actualizar el talento en la base de datos
        mongo.db.talentos.update_one(
            {'_id': ObjectId(id)}, {'$set': talento_actualizado})
        
        # Devolver la respuesta de éxito
        response = jsonify({'message': 'Talento ' + id + ' actualizado correctamente'})
        response.status_code = 200
        return response
    else:
        return not_found()
    
def agregar_indicador(mongo, talent_id, valor, descripcion):
    fecha = datetime.datetime.utcnow()
    indicador = {
        'fecha': fecha,
        'valor': valor,
        'descripcion': descripcion
    }
    result = mongo.db.talentos.update_one(
        {'_id': ObjectId(talent_id)},
        {'$push': {'indicadores': indicador}}
    )
    if result.modified_count == 0:
        return jsonify({'error': 'No se pudo agregar el indicador'}), 500
    return jsonify({'message': 'Indicador agregado exitosamente'}), 200

def obtener_indicadores(mongo, talent_id):
    talento = mongo.db.talentos.find_one({'_id': ObjectId(talent_id)})
    if not talento:
        return jsonify({'error': 'Talento no encontrado'}), 404
    indicadores = talento.get('indicadores', [])
    return jsonify({'indicadores': indicadores}), 200

def calcular_evaluacion(mongo, talent_id):
    talento = mongo.db.talentos.find_one({'_id': ObjectId(talent_id)})
    if not talento:
        return jsonify({'error': 'Talento no encontrado'}), 404
    indicadores = talento.get('indicadores', [])
    puntaje_total = sum(ind['valor'] for ind in indicadores)
    estado = determinar_estado(puntaje_total)
    return jsonify({'puntaje_total': puntaje_total, 'estado': estado}), 200

def determinar_estado(puntaje):
    if puntaje <= -20:
        return 'Deficiente'
    elif -20 < puntaje <= -10:
        return 'Insuficiente'
    elif -10 < puntaje <= 0:
        return 'Normal'
    elif 0 < puntaje <= 10:
        return 'Regular'
    elif 10 < puntaje <= 20:
        return 'Bueno'
    else:
        return 'Excelente'
    
# Actualizar indicador de talento
def update_talent_indicator(mongo, talent_id, indicator_id, value):
    try:
        result = mongo.db.talentos.update_one(
            {"_id": ObjectId(talent_id), "indicadores._id": ObjectId(indicator_id)},
            {"$set": {"indicadores.$.valor": value}}
        )
        if result.matched_count == 0:
            return jsonify({"error": "Talento o indicador no encontrado"}), 404
        return jsonify({"message": "Indicador actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

########################################################
def not_found(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
