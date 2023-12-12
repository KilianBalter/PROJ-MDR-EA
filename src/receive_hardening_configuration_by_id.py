import requests


def get_hardening_configuration_template_by_id(token, id):
    url = 'http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/dtools/DscApplicationConfigTemplate/'+id
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
        return response.json()['codeTemplate']
    else:
        print(f"Error: {response.status_code} - {response.text}")
