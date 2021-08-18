import json

def load_food_emissions():
    f = open('food_emissions.json')
    file_json = json.load(f)

    data = {}
    for item in file_json:
        data[item['food']] = item['emissions_estimate']

    return data
