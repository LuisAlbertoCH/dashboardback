import xml.etree.ElementTree as ET
from flask import jsonify, request, Response
from bson import ObjectId, json_util
import json

# Función para generar el XML basado en los datos de MongoDB
def xml(mongo):
    # Crear el nodo raíz del XML
    root = ET.Element("DatosCibercom")

    # Subnodo para talentos
    talentos_node = ET.SubElement(root, "Talentos")
    talentos = mongo.db.talentos.find()
    for talento in talentos:
        talento_node = ET.SubElement(talentos_node, "Talento")
        ET.SubElement(talento_node, "ID").text = str(talento["_id"])
        ET.SubElement(talento_node, "Nombre").text = talento.get("Nombre", "Desconocido")
        ET.SubElement(talento_node, "Apellidos").text = f"{talento.get('ApelPaterno', 'Desconocido')} {talento.get('ApelMaterno', 'Desconocido')}"
        ET.SubElement(talento_node, "FechaNacimiento").text = talento.get("FecNacimiento", "Desconocido")
        ET.SubElement(talento_node, "Fotografia").text = talento.get("Fotografia", "No disponible")

    # Subnodo para proyectos
    proyectos_node = ET.SubElement(root, "Proyectos")
    proyectos = mongo.db.proyectos.find()
    for proyecto in proyectos:
        proyecto_node = ET.SubElement(proyectos_node, "Proyecto")
        ET.SubElement(proyecto_node, "ID").text = str(proyecto["_id"])
        ET.SubElement(proyecto_node, "Nombre").text = proyecto.get("Nombre", "Desconocido")
        ET.SubElement(proyecto_node, "Descripcion").text = proyecto.get("Descripcion", "No disponible")
        ET.SubElement(proyecto_node, "EstadoDesarrollo").text = proyecto.get("EstadoDesarrollo", "Desconocido")
        ET.SubElement(proyecto_node, "Pagado").text = "Sí" if proyecto.get("Pagado", False) else "No"

        # Agregar tareas dentro de cada proyecto
        tareas_node = ET.SubElement(proyecto_node, "Tareas")
        tareas = mongo.db.tareas.find({"proyecto_id": proyecto["_id"]})
        for tarea in tareas:
            tarea_node = ET.SubElement(tareas_node, "Tarea")
            ET.SubElement(tarea_node, "Nombre").text = tarea.get("Nombre", "Desconocido")
            ET.SubElement(tarea_node, "Descripcion").text = tarea.get("Descripcion", "No disponible")
            ET.SubElement(tarea_node, "FechaInicio").text = tarea.get("FechaInicio", "Desconocido")
            ET.SubElement(tarea_node, "FechaFin").text = tarea.get("FechaFin", "Desconocido")

    # Subnodo para indicadores
    indicadores_node = ET.SubElement(root, "Indicadores")
    indicadores = mongo.db.indicadores.find()
    for indicador in indicadores:
        indicador_node = ET.SubElement(indicadores_node, "Indicador")
        ET.SubElement(indicador_node, "ID").text = str(indicador["_id"])
        ET.SubElement(indicador_node, "TalentoID").text = str(indicador.get("talento_id", "Desconocido"))
        ET.SubElement(indicador_node, "Estatus").text = indicador.get("Estatus", "Desconocido")
        ET.SubElement(indicador_node, "TiempoEntrega").text = indicador.get("TiempoEntrega", "Desconocido")

    # Subnodo para ganancias
    ganancias_node = ET.SubElement(root, "Ganancias")
    ganancias = mongo.db.ganancias.find()
    for ganancia in ganancias:
        ganancia_node = ET.SubElement(ganancias_node, "Ganancia")
        ET.SubElement(ganancia_node, "ID").text = str(ganancia["_id"])
        ET.SubElement(ganancia_node, "TotalIngresos").text = str(ganancia.get("TotalIngresos", 0))
        ET.SubElement(ganancia_node, "GastosProyecto").text = str(ganancia.get("GastosProyecto", 0))
        ET.SubElement(ganancia_node, "GastosOperacion").text = str(ganancia.get("GastosOperacion", 0))
        ET.SubElement(ganancia_node, "GananciaNeta").text = str(ganancia.get("GananciaNeta", 0))

    # Subnodo para impuestos
    impuestos_node = ET.SubElement(root, "Impuestos")
    impuestos = mongo.db.impuestos.find()
    for impuesto in impuestos:
        impuesto_node = ET.SubElement(impuestos_node, "Impuesto")
        ET.SubElement(impuesto_node, "EntidadFederativa").text = impuesto.get("EntidadFederativa", "Desconocido")
        ET.SubElement(impuesto_node, "SAT").text = str(impuesto.get("SAT", 0))
        ET.SubElement(impuesto_node, "IMSS").text = str(impuesto.get("IMSS", 0))
        ET.SubElement(impuesto_node, "GananciaCalculada").text = str(impuesto.get("GananciaCalculada", 0))

    # Convertir el árbol XML a bytes
    xml_data = ET.tostring(root, encoding="utf-8", method="xml")

    # Crear la respuesta HTTP con el archivo XML
    response = Response(xml_data, mimetype="application/xml")
    response.headers.set("Content-Disposition", "attachment", filename="DatosCibercom.xml")
    return response

########################################################
def not_found(error=None):
    message = {
        'message': 'Resource Not Found: ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
