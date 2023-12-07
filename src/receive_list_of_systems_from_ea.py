import requests
import json

import src.obtain_a_JWT_token as Jwt

def get_list_of_systems_from_ea(token):
    url = 'http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/ibase/server'
    credentials = 'Bearer ' + token

    headers = {
        'Nfclient': 'nftestapi',
        'Content-Type': 'application/json',
        'Authorization': credentials,
        'Method': 'GET'
    }

    # call might only work with verify=False because SSL certificate is untrusted
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response
    else:
        print(f"Error: {response.status_code} - {response.text}")
