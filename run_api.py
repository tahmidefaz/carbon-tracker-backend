from flask import Flask
from flask_restful import Resource, Api

from api.api_operations import Ping, Activity, Footprint

app = Flask(__name__)
api = Api(app)


api.add_resource(Ping, '/ping', '/ping/')
api.add_resource(Activity, '/activity', '/activity/')
api.add_resource(Footprint, '/footprint', '/footprint/')

if __name__ == '__main__':
    app.run(debug=True)
