import requests
import json
import base64
import os
import uuid
from dotenv import load_dotenv
import datetime
from geopy.geocoders import Nominatim

load_dotenv()

api_key = os.getenv("API_KEY")
api_secret = os.getenv('API_SECRET')

credentials = f"{api_key}:{api_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

#Retriving access token to access NSW Fuel APIs
def retrieve_access_token(authorization):
    url = "https://api.onegov.nsw.gov.au/oauth/client_credential/accesstoken"
    querystring = {
        "grant_type":"client_credentials"
    }
    headers = {
        'content-type': "application/json",
        'authorization': f"Basic {authorization}"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    data = response.json()

    return data["access_token"]

access_token = retrieve_access_token(encoded_credentials)

def retrieve_nearby_fuel_prices(latitude, longitude, fueltype="U91", radius=5):
    url = "https://api.onegov.nsw.gov.au/FuelPriceCheck/v1/fuel/prices/nearby"

    payload = {
        "fueltype": fueltype,
        "brand": [],
        "namedlocation": "",
        "latitude": latitude,
        "longitude": longitude,
        "radius": radius,
        "sortby": "Price",
        "sortascending": True
    }

    headers = {
        'authorization': f"Bearer {access_token}",
        'apikey': api_key,
        'content-type': "application/json",
        'transactionid': f"{uuid.uuid4()}",
        'requesttimestamp': f"{datetime.datetime.now()}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data = response.json()

    with open("nearby_prices.json", "w") as file:
        file.write(json.dumps(data, indent=4))
