import requests
import json


def get_rule_by_instance_name(token: str, instance_name: str):
    url = "http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/v3/hardeningengine/HardeningDsc/instanceRules"

    # Define the headers for the request
    headers = {
        'Nfclient': 'nftestapi',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
        'Method': 'POST'
    }

    # Define the data for the request
    data = {
        'instanceNames': [instance_name]
    }

    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            return get_rule_by_rule_id(token, str(response.json()['resolvedRules'][0]['includedBy'][0]['ruleId']))
        else:
            print(f"Error {response.status_code}: Failed to retrieve JWT token")

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_rule_by_rule_id(token: str, rule_id: str):
    url = 'http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/v3/benchmarkengine/Rules/' + rule_id
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
        return response.json()['settings']
    else:
        print(f"Error: {response.status_code} - {response.text}")
