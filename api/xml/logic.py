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
        ET.SubElement(talento_node, "Nombre").text = talento["Nombre"]
        ET.SubElement(talento_node, "Apellidos").text = f"{talento['ApelPaterno']} {talento['ApelMaterno']}"
        ET.SubElement(talento_node, "FechaNacimiento").text = talento["FecNacimiento"]
        ET.SubElement(talento_node, "Fotografia").text = talento.get("Fotografia", "")

    # Subnodo para proyectos
    proyectos_node = ET.SubElement(root, "Proyectos")
    proyectos = mongo.db.proyectos.find()
    for proyecto in proyectos:
        proyecto_node = ET.SubElement(proyectos_node, "Proyecto")
        ET.SubElement(proyecto_node, "ID").text = str(proyecto["_id"])
        ET.SubElement(proyecto_node, "Nombre").text = proyecto["Nombre"]
        ET.SubElement(proyecto_node, "Descripcion").text = proyecto["Descripcion"]
        ET.SubElement(proyecto_node, "EstadoDesarrollo").text = proyecto["EstadoDesarrollo"]
        ET.SubElement(proyecto_node, "Pagado").text = "Sí" if proyecto["Pagado"] else "No"

        # Agregar tareas dentro de cada proyecto
        tareas_node = ET.SubElement(proyecto_node, "Tareas")
        tareas = mongo.db.tareas.find({"proyecto_id": proyecto["_id"]})
        for tarea in tareas:
            tarea_node = ET.SubElement(tareas_node, "Tarea")
            ET.SubElement(tarea_node, "Nombre").text = tarea["Nombre"]
            ET.SubElement(tarea_node, "Descripcion").text = tarea["Descripcion"]
            ET.SubElement(tarea_node, "FechaInicio").text = tarea["FechaInicio"]
            ET.SubElement(tarea_node, "FechaFin").text = tarea["FechaFin"]

    # Subnodo para indicadores
    indicadores_node = ET.SubElement(root, "Indicadores")
    indicadores = mongo.db.indicadores.find()
    for indicador in indicadores:
        indicador_node = ET.SubElement(indicadores_node, "Indicador")
        ET.SubElement(indicador_node, "ID").text = str(indicador["_id"])
        ET.SubElement(indicador_node, "TalentoID").text = str(indicador["talento_id"])
        ET.SubElement(indicador_node, "Estatus").text = indicador["Estatus"]
        ET.SubElement(indicador_node, "TiempoEntrega").text = indicador["TiempoEntrega"]

    # Subnodo para ganancias
    ganancias_node = ET.SubElement(root, "Ganancias")
    ganancias = mongo.db.ganancias.find()
    for ganancia in ganancias:
        ganancia_node = ET.SubElement(ganancias_node, "Ganancia")
        ET.SubElement(ganancia_node, "ID").text = str(ganancia["_id"])
        ET.SubElement(ganancia_node, "TotalIngresos").text = str(ganancia["TotalIngresos"])
        ET.SubElement(ganancia_node, "GastosProyecto").text = str(ganancia["GastosProyecto"])
        ET.SubElement(ganancia_node, "GastosOperacion").text = str(ganancia["GastosOperacion"])
        ET.SubElement(ganancia_node, "GananciaNeta").text = str(ganancia["GananciaNeta"])

    # Subnodo para impuestos
    impuestos_node = ET.SubElement(root, "Impuestos")
    impuestos = mongo.db.impuestos.find()
    for impuesto in impuestos:
        impuesto_node = ET.SubElement(impuestos_node, "Impuesto")
        ET.SubElement(impuesto_node, "EntidadFederativa").text = impuesto["EntidadFederativa"]
        ET.SubElement(impuesto_node, "SAT").text = str(impuesto["SAT"])
        ET.SubElement(impuesto_node, "IMSS").text = str(impuesto["IMSS"])
        ET.SubElement(impuesto_node, "GananciaCalculada").text = str(impuesto["GananciaCalculada"])

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
