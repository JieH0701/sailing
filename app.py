from flask_restful import Api, Resource
from flask import Flask, jsonify, request

app = Flask(__name__)
api = Api(app)

marinas = {
    'grado': {
        'name': 'Marina Grado',
        'latitude': '45.6776922',
        'longitude': '13.3864432'},
    'pula': {
        'name': 'Marina Pula',
        'latitude': '44.8702281',
        'longitude': '13.8455311'},
    'izola': {
        'name': 'Marina Izola',
        'latitude': '45.53449655',
        'longitude': '13.655634754702382'},

}


class Marinas(Resource):
    def get(self, name):
        if name.lower() in marinas:
            return jsonify({name: marinas.get(name)})
        else:
            return {'message': f'Maria {name} is not in database'}, 404

    def post(self, name):
        request_data = request.get_json()
        marina = {
            'name': request_data['name'],
            'latitude': request_data['latitude'],
            'longitude': request_data['longitude']
        }
        marinas.update({name: marina})
        return marina, 201


api.add_resource(Marinas, '/marinas/<string:name>')

app.run(port=5000, debug=True)
