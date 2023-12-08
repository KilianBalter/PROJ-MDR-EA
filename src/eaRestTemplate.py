import requests


def ea_rest_call(call, methodtype, token, payload=None):
    url = 'https://win-jtn7m3lf4bq.theagleenforce.local:5001' + call
    credentials = 'Bearer ' + token

    headers = {
        'Nfclient': 'nftestapi',
        'Content-Type': 'application/json',
        'Authorization': credentials,
        'Method': methodtype
    }

    # call might only work with verify=False because SSL certificate is untrusted
    response = requests.get(url, headers=headers, params=payload)

    if response.status_code == 200:
        data = response.json()
        print(data)
    else:
        print(f"Error: {response.status_code} - {response.text}")


testcall = '/api/ibase/domain/2'  # example call
testmethodtype = 'GET'
testtoken = ''  # insert token here
testpayload = ''  # insert your payload here

# call without payload
ea_rest_call(testcall, testmethodtype, testtoken)
