from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from main import display_info
from fuel_api import retrieve_nearby_fuel_prices
from fuel_api_victoria import retrieve_victorian_fuel_prices, calculate_distance
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

agent = Nominatim(user_agent="Geopy Library")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development only
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/location")
def get_coordinates(location: str):
    coordinates = agent.geocode(location)
    return {"latitude": coordinates.latitude, "longitude": coordinates.longitude}

@app.get("/stations")
def get_stations(location: str, fuel_type: str, distance: int):
    coordinates = agent.geocode(location)
    
    retrieve_nearby_fuel_prices(coordinates.latitude, coordinates.longitude, fuel_type, distance)
    display = display_info(fuel_type, distance)
    
    details = []
    for station in display:
        station_dict = {}

        station_dict["name"] = station["name"]
        station_dict["address"] = station["address"]
        station_dict["latitude"] = station["location"]["latitude"]
        station_dict["longitude"] = station["location"]["longitude"]
        station_dict["distance"] = station["location"]["distance"]
        station_dict["fuel_type"] = station["fueltype"]
        station_dict["price"] = station["price"]
        details.append(station_dict)
    return details

@app.get("/stations_victoria")
def get_stations_victoria(location: str, fuel_type: str, distance: int):
    coordinates = agent.geocode(location)

    fuel_prices = retrieve_victorian_fuel_prices()
    stations = calculate_distance(coordinates.latitude, coordinates.longitude, fuel_prices, distance)
    details = []
    for station in stations:
        for price_details in station['fuelPrices']:
            station_dict = {}

            distance = geodesic(coordinates, (station['fuelStation']['location']['latitude'], station['fuelStation']['location']['longitude']))

            station_dict["name"] = station['fuelStation']['name']
            station_dict["address"] = station['fuelStation']['address']
            station_dict["latitude"] = station['fuelStation']['location']['latitude']
            station_dict["longitude"] = station['fuelStation']['location']['longitude']
            station_dict["distance"] = distance
            station_dict["fuel_type"] = station['fuelPrices']['fuelType']
            station_dict["price"] = station['fuelPrices']['price']
            details.append(station_dict)
    return details