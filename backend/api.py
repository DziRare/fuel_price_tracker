from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from main import display_info
from fuel_api import retrieve_nearby_fuel_prices
from geopy.geocoders import Nominatim

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
