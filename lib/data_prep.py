import requests
from requests.exceptions import HTTPError

from flask import abort

from lib.config import config
from lib.food_emi_provider import load_food_emissions


food_emmisions = load_food_emissions()


def get_car_emissions(car_data):
    mpg_map = {"compact": 44.9741, "midrange": 35.10664, "heavy": 28.0351}
    fuel_co2_map = {"petrol": 10.86, "diesel": 11.91}

    car_mpg = mpg_map[car_data["type"]]
    fuel_co2 = fuel_co2_map[car_data["fuel_type"]]

    emission = (fuel_co2/car_mpg)*int(car_data["distance"])

    data = {"name": "car"}
    data["info"] = f"{car_data['type']} {car_data['fuel_type']} {car_data['distance']}mi"
    data["emission"] = round(emission,2)

    return data
    

def get_electricity_emissions(electricity_data):
    emission = int(electricity_data["kwh"]) * 0.4532

    data = {"name": "electricity"}
    data["info"] = f"{electricity_data['kwh']} kwh"
    data["emission"] = round(emission,2)

    return data


def fetch_flight_emission(flight_data):
    params = {'segments[0][origin]':flight_data['origin'], 'segments[0][destination]':flight_data['destination'], 'cabin_class':flight_data['cabin_class'], 'currencies[]':'USD'}
    
    response = requests.get(config['goclimate_endpoint'], auth=(config['goclimate_key'],None), data=params)
    response.raise_for_status()
    response_json = response.json()

    return response_json['footprint']


def get_flight_emissions(flight_data):
    emission = fetch_flight_emission(flight_data)

    data = {"name": "flight"}
    data["info"] = f"{flight_data['origin']} - {flight_data['destination']} {flight_data['cabin_class']} class"
    data["emission"] = round(emission,2)

    return data


def get_food_emissions(food_data):
    emission_per_gram = float(food_emmisions[food_data['type']])
    emission = (float(food_data['weight'])*emission_per_gram)/1000

    data = {"name": "food"}
    data["info"] = f"{food_data['type']} {food_data['weight']} g"
    data["emission"] = round(emission,2)
    print(data)
    return data


def produce_db_data(args):
    if args['name'] == 'car':
        car_data = args.get('car_data')

        if not car_data:
            abort(400, description="car_data is missing.")
        if car_data["type"] not in ["compact","midrange","heavy"]:
            abort(400, description="invalid car type")
        if car_data["fuel_type"] not in ["petrol","diesel"]:
            abort(400, description="invalid fuel type")

        return get_car_emissions(car_data)

    elif args['name'] == 'electricity':
        electricity_data = args.get('electricity_data')

        if not electricity_data:
            abort(400, description="electricity_data is missing")
        if not electricity_data.get('kwh'):
            abort(400, description="kwh in electricity_data is missing")

        return get_electricity_emissions(electricity_data)

    elif args['name'] == 'flight':
        flight_data = args.get('flight_data')

        if not flight_data:
            abort(400, description="flight_data is missing")
        if "origin" not in flight_data or "destination" not in flight_data or "cabin_class" not in flight_data:
            abort(400, description="fields are missing in flight_data")
        if flight_data['cabin_class'] not in ['economy','premium_economy','business','first']:
            abort(400, description="invalid cabin_class")
        
        return get_flight_emissions(flight_data)
    

    elif args['name'] == 'food':
        food_data = args.get('food_data')

        if not food_data:
            abort(400, description="food_data is missing")
        if "type" not in food_data or "weight" not in food_data:
            abort(400, description="fields are missing in food_data")

        return get_food_emissions(food_data)
    
    else:
        abort(400)

    return
