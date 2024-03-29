from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from application.models.course_model import CourseModel
from application.resources.location import Location


class Course(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'date',
        type=str,
        required=True,
        help='Every course calculation needs a date')
    parser.add_argument(
        'start_name',
        type=str,
        required=True,
        help='Every course calculation needs a start position')
    parser.add_argument(
        'end_name',
        type=str,
        required=True,
        help='Every course calculation needs a end position')

    @jwt_required()
    def get(self):
        data = Course.parser.parse_args()
        courses = CourseModel.find_by_date(data['date'])
        if courses:
            return courses
        else:
            return {'message': "An course with this date '{}' does not exist.".format(data['date'])}, 404

    def post(self):
        data = Course.parser.parse_args()
        if CourseModel.find_course(data['date'], data['start_name'], data['end_name']):
            return {'message': "An course with start position '{}' already exists.".format(data['start_name'])}, 400

        Location.post(data['start_name'])
        Location.post(data['end_name'])
        course = CourseModel(data['date'], data['start_name'], data['end_name'])
        try:
            course.save_to_db(), 201
            return {'message': "An course is created"}
        except:
            return {'message': "An error occurred inserting the course '{}'.".format(data['start_name'])}, 500

    def delete(self):
        data = Course.parser.parse_args()
        course = CourseModel.find_course(data['date'], data['start_name'], data['end_name'])
        if course:
            course.delet_from_db()
            return {'message': 'Course deleted'}


class CourseList(Resource):
    def get(self):
        return {'course': [course.json() for course in CourseModel.query.all()]}
