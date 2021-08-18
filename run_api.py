from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from lib.config import init_config, config

from api.api_operations import Ping, Activity, Footprint

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)

init_config()

api.add_resource(Ping, '/ping', '/ping/')
api.add_resource(Activity, '/activity', '/activity/')
api.add_resource(Footprint, '/footprint', '/footprint/')

port = config['port']
if __name__ == '__main__':
    app.run(threaded=True, debug=True, host='0.0.0.0', port=port)
