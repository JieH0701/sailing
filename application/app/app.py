from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity
from application.resources.user import UserRegister
from application.resources.location import Location, LocationList
from application.resources.course import Course, CourseList
from application.db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'test'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Location, '/location/<string:name>')
api.add_resource(LocationList, '/locations')
api.add_resource(Course, '/course/<string:name>')
api.add_resource(CourseList, '/courses')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
