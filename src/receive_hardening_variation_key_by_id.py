import requests
import json

import src.obtain_a_JWT_token as Jwt
import src.receive_list_of_systems_from_ea as Los


# main function
def get_hardening_variation_key_by_id(token, server_id):
    dsc_server_id = get_dsc_server_id(token, server_id)
    dsc_server_application = get_dsc_server_application(token, server_id)
    data = dsc_server_application.json()
    for dsc in data:
        return dsc["variationKey"]


# function to receive the dscServerId
def get_dsc_server_id(token, id_1):
    url = f'http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/dtools/DscServer/{id_1}'
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
        return response.json()["serverId"]

    else:
        print(f"Error: {response.status_code} - {response.text}")


# function to receive the application information. variation key is part of it
def get_dsc_server_application(token, dsc_id):
    url = f'http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/dtools/DscServerApplication/dscserver/{dsc_id}'
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
        print(f"Dsc Application Error: {response.status_code} - {response.text}")

#example server_id = 1
#erg = get_hardening_variation_key_by_id(Jwt.get_jwt_token("username","password"),server_id)
#print(erg)
