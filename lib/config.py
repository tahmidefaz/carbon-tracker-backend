import json
import os

config = {}

def get_api_key(name):
    file_obj = open('misc-keys.json',)
    
    data = json.load(file_obj)
    file_obj.close()
    return data[name]

def init_config():
    config['port'] = int(os.environ.get('PORT', 5000))
    config['goclimate_endpoint'] = 'https://api.goclimate.com/v1/flight_footprint'
    config['goclimate_key'] = get_api_key('goclimate_key')

