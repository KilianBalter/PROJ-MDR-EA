import requests


def ea_rest_call(call: str, methodtype: str, token: str, payload=None):
    url = 'https://win-jtn7m3lf4bq.theagleenforce.local:5001' + call
    credentials = 'Bearer ' + token

    headers = {
        'Nfclient': 'nftestapi',
        'Content-Type': 'application/json',
        'Authorization': credentials,
        'Method': methodtype
    }

    # call might only work with verify=False because SSL certificate is untrusted
    response = requests.get(url, headers=headers, params=payload, verify=False)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error reaching API at {url}: \nCode: {response.status_code} \nResponse: {response.text}")
