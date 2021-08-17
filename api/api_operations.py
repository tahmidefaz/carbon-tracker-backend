from flask_restful import Resource, reqparse

from flask_restful import reqparse

parser = reqparse.RequestParser()

class Ping(Resource):
    def get(self):
        return {'message': 'pong'}

class Activity(Resource):
    def __init__(self):
        self.parser = parser.copy()
        self.parser.add_argument('x-identity', location='headers', required=True, help="x-identity header was not provided")

    def post(self):
        args = self.parser.parse_args()
        print("account", args['x-identity'])
        return {'message': 'success'}, 201


class Footprint(Resource):
    def __init__(self):
        self.parser = parser.copy()
        self.parser.add_argument('x-identity', location='headers', required=True, help="x-identity header was not provided")
        self.parser.add_argument('page', type=int, default=1, help="page param must be a integer")
        self.parser.add_argument('limit', type=int, default=10, help="limit param must be a integer")

    def get(self):
        args = self.parser.parse_args()
        page = args.get('page')
        limit = args.get('limit')

        response = {"page": page, "limit": limit, "total": 10, "data": []}
        return response
