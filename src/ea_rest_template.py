import requests
import json


# Function to make an API-Call to the EA
def ea_rest_call(endpoint: str, methodtype: str, token: str, params=None, data=None):
    url = 'http://win-jtn7m3lf4bq.theagleenforce.local:5000' + endpoint
    credentials = 'Bearer ' + token

    headers = {
        'Nfclient': 'nftestapi',
        'Content-Type': 'application/json',
        'Authorization': credentials
    }

    response = requests.request(methodtype, url, headers=headers, params=params, data=json.dumps(data))

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error reaching API at {url}: \nCode: {response.status_code} \nResponse: {response.headers}")