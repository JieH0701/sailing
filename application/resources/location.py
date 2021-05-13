from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from application.models.location_model import LocationModel


class Location(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='Every course needs a name')

    @jwt_required()
    def get(self, name):
        location = LocationModel.find_by_name(name)
        if location:
            return location.json()
        else:
            return {'message': "An course with name '{}' hasn't saved in Database.".format(name)}, 404

    @staticmethod
    def post(name):
        if LocationModel.find_by_name(name):
            return {'message': "An course with name '{}' already exists.".format(name)}, 400
        location = LocationModel.get_location_by_name(name)
        try:
            location.save_to_db(), 201
            return {'message': "An course with name '{}' is created".format(name)}
        except:
            return {'message': "An error occurred inserting the item '{}'.".format(name)}, 500

    def delete(self, name):
        location = LocationModel.find_by_name(name)
        if location:
            location.delet_from_db()
        return {'message': "SailingCourse '{}' deleted".format(name)}

    # def put(self):
    #     course = LocationModel.find_by_name(self.name)
    #     if course is None:
    #         course = LocationModel(self.name)
    #     else:
    #         course.latitude = self.data['latitude']
    #         course.longtitude = self.data['longtitude']
    #     course.save_to_db()
    #     return course.json()


class LocationList(Resource):
    def get(self):
        return {'locations': [location.json() for location in LocationModel.query.all()]}
