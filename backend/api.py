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

# NSW and Victoria use different codes for diesel
VIC_FUEL_CODES = {"DL": "DSL", "PDL": "PDSL"}
@app.get("/stations_victoria")
def get_stations_victoria(location: str, fuel_type: str, distance: int):
    coordinates = agent.geocode(location)
    vic_fuel_type = VIC_FUEL_CODES.get(fuel_type, fuel_type)

    fuel_prices = retrieve_victorian_fuel_prices()
    stations = calculate_distance(coordinates.latitude, coordinates.longitude, fuel_prices, distance)
    details = []
    for station in stations:
        info = station["fuelStation"]
        lat = info["location"]["latitude"]
        lon = info["location"]["longitude"]
        km = round(geodesic((coordinates.latitude, coordinates.longitude), (lat, lon)).km, 2)
        for price_details in station['fuelPrices']:
            if price_details["fuelType"] != vic_fuel_type:
                continue
            if not price_details.get("isAvailable", True) or price_details.get("price") is None:
                continue

            station_dict = {}
            station_dict["name"] = station['fuelStation']['name']
            station_dict["address"] = station['fuelStation']['address']
            station_dict["latitude"] = lat
            station_dict["longitude"] = lon
            station_dict["distance"] = km
            station_dict["fuel_type"] = fuel_type
            station_dict["price"] = price_details['price']
            details.append(station_dict)
    return details