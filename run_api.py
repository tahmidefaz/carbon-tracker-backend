import os

from flask import Flask
from flask_restful import Resource, Api

from api.api_operations import Ping, Activity, Footprint

app = Flask(__name__)
api = Api(app)


api.add_resource(Ping, '/ping', '/ping/')
api.add_resource(Activity, '/activity', '/activity/')
api.add_resource(Footprint, '/footprint', '/footprint/')

port = int(os.environ.get('PORT', 5000))
if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
