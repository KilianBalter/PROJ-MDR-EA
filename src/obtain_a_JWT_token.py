import requests
import json


def get_jwt_token(username, password):
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

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        if response.status_code == 200:
            return response.json().get('token')
        else:
            print(f"Error {response.status_code}: Failed to retrieve JWT token")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# Example usage
username = ''
password = ''
jwt_token = get_jwt_token(username, password)

if jwt_token:
    print(f"JWT Token: {jwt_token}")
else:
    print("JWT Token retrieval failed.")
