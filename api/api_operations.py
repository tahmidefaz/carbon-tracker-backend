import uuid

from flask_restful import Resource, reqparse
from firebase_admin import credentials, firestore, initialize_app
from flask import request, jsonify

from lib.data_prep import produce_db_data
from lib.config import config



cred = credentials.Certificate('carbon-tracker-key.json')
default_app = initialize_app(cred)
db = firestore.client()
db_ref = db.collection('accounts')


parser = reqparse.RequestParser()

class Ping(Resource):
    def get(self):
        return {'message': 'pong'}

class Activity(Resource):
    def __init__(self):
        self.parser = parser.copy()
        self.parser.add_argument('x-identity', location='headers', required=True, help="x-identity header was not provided")
        self.parser.add_argument(
            'name',
            choices=('car','electricity'),
            location='json', required=True, help='activity name was not provided'
            )
        self.parser.add_argument('date', type=str, location='json', required=True, help='date was not provided')
        self.parser.add_argument('car_data', type=dict, location='json')
        self.parser.add_argument('electricity_data', type=dict, location='json')
        # self.parser.add_argument('food_data', type=dict, location='json')

    def post(self):
        try:
            args = self.parser.parse_args()
            account = args['x-identity']

            activity_data = produce_db_data(args)

            document_id = uuid.uuid4().hex[:6].upper()
            db_ref.document(account).collection(args['date']).document(document_id).set(activity_data)

            return {'message': 'success'}, 201
        except Exception as e:
            return {'message': f"An Error Occured: {e}"}, 400


class Footprint(Resource):
    def __init__(self):
        self.parser = parser.copy()
        self.parser.add_argument('x-identity', location='headers', required=True, help="x-identity header was not provided")
        self.parser.add_argument('page', type=int, default=1, help="page param must be a integer")
        self.parser.add_argument('limit', type=int, default=10, help="limit param must be a integer")

    def get(self):
        try:
            args = self.parser.parse_args()
            page = args.get('page')
            limit = args.get('limit')
            
            account = args['x-identity']
            collections = db_ref.document(account).collections()

            response_data = []
            for collection in collections:
                activity_array = []
                for activity in collection.stream():
                    activity_array.append(activity.to_dict())

                response_data.append({collection.id: activity_array})

            response = {"page": page, "limit": limit, "total": 10, "data": response_data}
            return response
        except Exception as e:
            return {'message': f"An Error Occured {e}"}, 400
