from flask import jsonify, request, Response
from bson import json_util
from bson.objectid import ObjectId
import json

def json_handler(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

######################################################
# PROYECTOS

# Crear proyecto
def create_proyecto(mongo):
    try:
        data = request.json
        nombre_proyecto = data.get('NombreProyecto')
        descripcion = data.get('Descripcion')
        fecha_inicio = data.get('FechaInicio')
        fecha_fin = data.get('FechaFin')
        talentos = data.get('Talentos', [])  # Lista de IDs de talentos
        presupuesto = data.get('Presupuesto', 0)  # Nuevo campo
        pago = data.get('Pago', False)
        estatus = data.get('Estatus', 'Pendiente')
        ingreso = float(data.get('Ingreso', 0))

        if nombre_proyecto:
            proyecto = {
                'NombreProyecto': nombre_proyecto,
                'Descripcion': descripcion,
                'FechaInicio': fecha_inicio,
                'FechaFin': fecha_fin,
                'Talentos': talentos,
                'Presupuesto': presupuesto,  # Guardamos el presupuesto
                'Pago': pago,
                'Estatus': estatus,
                'Ingreso': ingreso
            }
            mongo.db.proyectos.insert_one(proyecto)
            return jsonify({"message": "Proyecto creado exitosamente"}), 201
        else:
            return jsonify({"error": "Nombre del proyecto es obligatorio"}), 400
    except Exception as e:
        return jsonify({"error": "Error al crear el proyecto", "details": str(e)}), 500

# Obtener todos los proyectos
def get_proyectos(mongo):
    proyectos = mongo.db.proyectos.find()
    return Response(json_util.dumps(proyectos), mimetype="application/json")

# Obtener proyecto por ID
def get_proyecto(id, mongo):
    try:
        proyecto = mongo.db.proyectos.find_one({'_id': ObjectId(id)})
        if proyecto:
            return Response(json_util.dumps(proyecto), mimetype="application/json")
        else:
            return jsonify({"error": "Proyecto no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": "ID no válido", "details": str(e)}), 400

# Actualizar proyecto por ID
def update_proyecto(id, mongo):
    try:
        # Validar que el ID sea válido
        if not ObjectId.is_valid(id):
            return jsonify({"error": "ID no válido"}), 400

        data = request.json
        nombre_proyecto = data.get('NombreProyecto')
        descripcion = data.get('Descripcion')
        fecha_inicio = data.get('FechaInicio')
        fecha_fin = data.get('FechaFin')
        talentos = data.get('Talentos', [])
        presupuesto = data.get('Presupuesto', 0)
        pago = data.get('Pago', False)
        estatus = data.get('Estatus', 'Pendiente')
        ingreso = float(data.get('Ingreso', 0))

        # Validar el campo obligatorio
        if not nombre_proyecto:
            return jsonify({"error": "El nombre del proyecto es obligatorio"}), 400

        # Validar que los talentos sean válidos
        talento_ids = [ObjectId(t) for t in talentos if ObjectId.is_valid(t)]
        talentos_validos = list(mongo.db.talentos.find({"_id": {"$in": talento_ids}}))
        if len(talentos_validos) != len(talento_ids):
            return jsonify({"error": "Uno o más talentos proporcionados no son válidos"}), 400

        # Construir el objeto actualizado
        proyecto_actualizado = {
            'NombreProyecto': nombre_proyecto,
            'Descripcion': descripcion,
            'FechaInicio': fecha_inicio,
            'FechaFin': fecha_fin,
            'Talentos': talento_ids,
            'Presupuesto': presupuesto,
            'Pago': pago,
            'Estatus': estatus,
            'Ingreso': ingreso
        }

        # Intentar actualizar
        result = mongo.db.proyectos.update_one({'_id': ObjectId(id)}, {'$set': proyecto_actualizado})
        if result.matched_count == 1:
            return jsonify({'message': f'Proyecto {id} actualizado correctamente'}), 200
        else:
            return jsonify({"error": f"Proyecto con ID {id} no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al actualizar el proyecto", "details": str(e)}), 500


# Eliminar proyecto por ID
def delete_proyecto(id, mongo):
    try:
        print(f"ID recibido: {id}")  # Depuración para revisar qué llega
        if not id or not isinstance(id, str):
            return jsonify({"error": "ID inválido o no proporcionado"}), 400
        
        if not ObjectId.is_valid(id):
            return jsonify({"error": "ID no válido"}), 400

        result = mongo.db.proyectos.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': f'Proyecto {id} eliminado correctamente'}), 200
        else:
            return jsonify({"error": "Proyecto no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": "Error al eliminar el proyecto", "details": str(e)}), 500

########################################################
# Respuesta para recurso no encontrado
def not_found(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
