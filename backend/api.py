from fastapi import FastAPI
import uvicorn
from backend.main import display

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/stations")
def get_stations():
    details = []
    for station in display:
        station_dict = {}

        station_dict["name"] = station["name"]
        station_dict["address"] = station["address"]
        station_dict["distance"] = station["location"]["distance"]
        station_dict["fuel_type"] = station["fueltype"]
        station_dict["price"] = station["price"]
        details.append(station_dict)
    return details
