import requests
import json
import base64
import os
from dotenv import load_dotenv

# url = "https://jsonplaceholder.typicode.com/posts"
# response = requests.get(url)

# if response.status_code == 200:
#     print("Request was successful!")
#     data = response.json()
# else:
#     print(f"Failed to retrieve data. Status code: {response.status_code}")

# with open("station_data.json", "w") as file:
#     file.write(json.dumps(data, indent=4))

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv('CLIENT_SECRET')

credentials = f"{client_id}:{client_secret}"
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
