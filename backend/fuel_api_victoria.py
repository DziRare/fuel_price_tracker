import os
from dotenv import load_dotenv
import uuid
import requests
import json
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

load_dotenv()

api_key_vic = os.getenv("API_KEY_VIC")
agent = Nominatim(user_agent="victorian_fuel_prices")

def retrieve_victorian_fuel_prices():
    url = "https://api.fuel.service.vic.gov.au/open-data/v1/fuel/prices"

    headers = {
        'User-Agent': "application/json",
        'x-consumer-id': api_key_vic,
        'x-transactionid': f"{uuid.uuid4()}"
    }

    response = requests.request("GET", url, headers=headers)
    data = response.json()
    return data['fuelPriceDetails']

    # with open("nearby_prices_victoria.json", "w") as file:
    #     file.write(json.dumps(data, indent=4))

def calculate_distance(latitude, longitude, fuel_prices, radius):
    epicentre = (latitude, longitude)
    stations = []
    for station_info in fuel_prices:
        station_location = (station_info['fuelStation']['location']['latitude'], station_info['fuelStation']['location']['longitude'])
        distance = geodesic(epicentre, station_location)
        if distance <= radius:
            print(station_info['fuelStation']['name'])
            for details in station_info['fuelPrices']:
                print(f"{details['fuelType']}: {details['price']}")
            stations.append(station_info)
            print("-----------------------------------")

    return stations

fuel_prices = retrieve_victorian_fuel_prices()
location = agent.geocode(input("Enter location: "))
radius = float(input("Enter desired radius: "))
calculate_distance(location.latitude, location.longitude, fuel_prices, radius)
