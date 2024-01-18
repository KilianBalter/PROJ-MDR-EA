import requests
import json


def get_jwt_token(username: str, password: str):
    url = "http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/logon/LoginForms"

    # Define the headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    # Define the data for the request
    data = {
        'username': username,
        'password': password
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    response.raise_for_status()

    return response.json().get('token')
