import requests
import json
import base64
import os
import uuid
# from dotenv import load_dotenv
import datetime
from geopy.geocoders import Nominatim
from fuel_api import retrieve_nearby_fuel_prices

agent = Nominatim(user_agent="Geopy Library")

#Displaying information to the user
def display_info(fuel_type, distance):
    with open("nearby_prices.json") as file:
        data = json.load(file)
        fuel_stations = data['stations']
        fuel_prices = data['prices']

        for station in fuel_stations:
            for fuel in fuel_prices:
                if station['code'] == fuel['stationcode']:
                    station.update(fuel)
        print("\n--------------------------------------------------------------\n")
        print(f"Here are the nearest petrol stations that serve {fuel_type} fuel within a {distance}km radius:\n")
        for station in fuel_stations:
            print(f"Price: {station['price']}")
            print(f"Name: {station['name']}")
            print(f"Address: {station['address']}")
            print(f"Fuel: {station['fueltype']}")
            print(f"Distance from location: {station['location']['distance']}km \n")

        return fuel_stations


if __name__ == "__main__":
#Entering details to retrieve fuel data
    location = agent.geocode(input("Enter location: "))
    distance = ""
    if location:
        fuel = input("Enter fuel type you're looking for (DL, E10, P95, P98, U91, PDL, EV, LPG): ")
        if fuel in ["DL", "E10", "P95", "P98", "U91", "PDL", "EV", "LPG"]:
            while distance == "":
                try:
                    distance = int(input("Enter the distance (km) you would like the station to be in: "))
                except ValueError:
                    print("Distance must be integer value.")
            retrieve_nearby_fuel_prices(location.latitude, location.longitude, fuel, distance)
            display = display_info(fuel, distance)
        else:
            print("Invalid fuel type.")
    else:
        print("Location not found.")
