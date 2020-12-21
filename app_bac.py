from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Marina(Resource):
    def get(self, name):
        return {'marina': name}


marinas = [
    {
        'Grado': {
            'name': 'Marina Grado',
            'latitude': '45.6776922',
            'longitude': '13.3864432'},
        'Pula': {
            'name': 'Marina Pula',
            'latitude': '44.8702281',
            'longitude': '13.8455311'},
        'Izola': {
            'name': 'Marina Izola',
            'latitude': '45.53449655',
            'longitude': '13.655634754702382'}
    }
]


@app.route('/')
def home():
    return render_template('index.html')


# POST - used to receive data
# GET - used to send data back only

# POST /marina data: {name_}
@app.route('/marinas', methods=['POST'])
def create_marina():
    request_data = request.get_json()
    new_marina = {
        'name': 'Marina' + request_data['name'],
        'latitude': request_data['latitude'],
        'longitude': request_data['longitude']
    }
    marinas.append({request_data['name']: new_marina})
    return jsonify({request_data['name']: new_marina})


# GET /marina/<string:name>
# Iterate over marinas, if the name matches, return information, else none
@app.route('/marinas/<string:name>')
def get_marina(name):
    if name in marinas:
        return jsonify(marinas[name])
    else:
        return jsonify({'message': 'Maria location is not in database'})


# GET /marina
@app.route('/marinas')
def get_all_marinas():
    return jsonify({'marians': marinas})


# GTE /marina/<string:name>/position {name:, latitude:, longitude:}
@app.route('/marinas/<string:name>/latitude', methods=['GET'])
def get_latitude_from_marina(name):
    if name in marinas:
        return jsonify({'latitue': marinas[name]['latitue']})
    else:
        return jsonify({'message': 'Maria location is not in database'})


# GTE /marina/<string:name>/position {name:, latitude:, longitude:}
@app.route('/marinas/<string:name>/longitude', methods=['GET'])
def get_longitude_from_marina(name):
    if name in marinas:
        return jsonify({'longitude': marinas[name]['longitude']})
    else:
        return jsonify({'message': 'Maria location is not in database'})


app.run(port=5000)
