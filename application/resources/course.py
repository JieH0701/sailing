from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from application.models.course_model import CourseModel
from application.resources.location import Location


class Course(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.data = self.parser.parse_args()
        self.parser.add_argument(
            'date',
            type=str,
            required=True,
            help='Every course calculation needs a date')
        self.parser.add_argument(
            'start_name',
            type=str,
            required=True,
            help='Every course calculation needs a start position')

        self.parser.add_argument(
            'end_name',
            type=str,
            required=True,
            help='Every course calculation needs a end position')

    @jwt_required()
    def get(self):
        courses = CourseModel.find_by_date(self.data.get('date'))
        if courses:
            return courses
        else:
            return {'message': "An course with this date '{}' does not exist.".format(self.data.get('date'))}, 404

    def post(self):
        if CourseModel.find_course(self.data.get('date'), self.data.get('start_name'), self.data.get('end_name')):
            return {'message': "An course with name '{}' already exists.".format(self.data.get('date'))}, 400
        Location.post(self.data.get('start_name'))
        Location.post(self.data.get('end_name'))
        course = CourseModel(self.data.get('date'), self.data.get('start_name'), self.data.get('end_name'))
        try:
            course.save_to_db(), 201
        except:
            return {'message': "An error occurred inserting the course '{}'.".format(self.data.get('date'))}, 500

    def delete(self):
        course = CourseModel.find_course(self.data.get('date'), self.data.get('start_name'), self.data.get('end_name'))
        if course:
            course.delet_from_db()
        return {'message': 'Course deleted'}


class CourseList(Resource):
    def get(self):
        return {'course': [course.json() for course in CourseModel.query.all()]}
