from flask import abort

def get_car_emissions(car_data):
    mpg_map = {"compact": 44.9741, "midrange": 35.10664, "heavy": 28.0351}
    fuel_co2_map = {"petrol": 10.86, "diesel": 11.91}

    car_mpg = mpg_map[car_data["type"]]
    fuel_co2 = fuel_co2_map[car_data["fuel_type"]]

    emission = (fuel_co2/car_mpg)*int(car_data["distance"])

    data = {"name": "car"}
    data["info"] = car_data["type"] + " " + car_data["fuel_type"] + " " + car_data["distance"]+"mi"
    data["emission"] = round(emission,2)

    return data
    

def get_electricity_emissions(electricity_data):
    emission = int(electricity_data["kwh"]) * 0.4532

    data = {"name": "electricity"}
    data["info"] = electricity_data["kwh"] + " kwh"
    data["emission"] = round(emission,2)

    return data


def produce_db_data(args):
    # {"name":args['name'], "info": (args['name']+' '+args["food_data"]["amount"]),"emission": 40}
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
    return
