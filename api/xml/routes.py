from .logic import request
from .logic import (xml)

def setup_xml_route(app, mongo):
    @app.route('/xml', methods=['GET'])
    def xml_route():
        return xml(mongo)
