from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from application.models.course_model import CourseModel


class Course(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()

    @jwt_required()
    def get(self, name):
        store = CourseModel.find_by_name(name)
        if store:
            return store.json()
        else:
            return {'message': "An course with name '{}' does not exist.".format(name)}, 404

    def post(self, name):
        if CourseModel.find_by_name(name):
            return {'message': "An course with name '{}' already exists.".format(name)}, 400
        store = CourseModel(name)
        try:
            store.save_to_db(), 201
        except:
            return {'message': "An error occurred inserting the store '{}'.".format(name)}, 500

    def delete(self, name):
        course = CourseModel.find_by_name(name)
        if course:
            course.delet_from_db()
        return {'message': 'Course deleted'}


class CourseList(Resource):
    def get(self):
        return {'course': [course.json for course in CourseModel.query.all()]}
