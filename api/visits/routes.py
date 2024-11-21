from .logic import increment_visits, get_visits

def setup_visits_routes(app, mongo):
    @app.route('/visits', methods=['POST'])
    def increment_visits_route():
        return increment_visits(mongo)

    @app.route('/visits', methods=['GET'])
    def get_visits_route():
        return get_visits(mongo)
