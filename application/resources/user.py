from flask_restful import Resource, reqparse
from application.models.user_model import UserModel


class UserRegister(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument(
            'password',
            type=str,
            required=True,
            help='This feld can not be left blank!')
        self.parser.add_argument(
            'username',
            type=str,
            required=True,
            help='This feld can not be left blank!')

    def post(self):
        data = self.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message': "An User with name '{}' already exists.".format(data['username'])}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {'message': "An user with name '{}' is created".format(data['username'])}, 200
