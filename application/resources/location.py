from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from application.models.location_model import LocationModel
import navigation.get_geo_position as geo


class Location(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.data = self.parser.parse_args()
        self.parser.add_argument(
            'name',
            type=str,
            required=True,
            help='Every location needs a name')

    @jwt_required()
    def get(self, name):
        location = LocationModel.find_by_name(name)
        if location:
            return location.json()
        else:
            return {'message': "An location with name '{}' hasn't saved in Database.".format(name)}, 404

    def post(self, name):
        if LocationModel.find_by_name(name):
            return {'message': "An location with name '{}' already exists.".format(name)}, 400
        mygeo = geo.GetGeoPosition(name)
        loc = mygeo.get_geo_position(name)
        location = LocationModel(name, loc.longitude, loc.latitude)
        try:
            location.save_to_db(), 201
        except:
            return {'message': "An error occurred inserting the item '{}'.".format(name)}, 500

    def delete(self, name):
        location = LocationModel.find_by_name(name)
        if location:
            location.delet_from_db()
        return {'message': "Location '{}' deleted".format(name)}

    # def put(self):
    #     location = LocationModel.find_by_name(self.name)
    #     if location is None:
    #         location = LocationModel(self.name)
    #     else:
    #         location.latitude = self.data['latitude']
    #         location.longtitude = self.data['longtitude']
    #     location.save_to_db()
    #     return location.json()


class LocationList(Resource):
    def get(self):
        return {'locations': [location.json() for location in LocationModel.query.all()]}
