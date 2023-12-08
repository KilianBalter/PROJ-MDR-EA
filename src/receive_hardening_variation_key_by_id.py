from eaRestTemplate import ea_rest_call


# main function
def get_hardening_variation_key_by_id(token: str, server_id: str) -> str:
    if not server_id:
        return ''

    dsc_server_id = get_dsc_server_id(token, server_id)
    dsc_server_application = get_dsc_server_application(token, dsc_server_id)
    for dsc in dsc_server_application:
        return dsc["variationKey"]


# Function to receive the dscServerId
def get_dsc_server_id(token, id_1):
    response = ea_rest_call(f'/api/dtools/DscServer/{id_1}', 'GET', token)
    return response["serverId"]


# Function to receive the application information. Variation key is part of it
def get_dsc_server_application(token, dsc_id):
    return ea_rest_call(f'/api/dtools/DscServerApplication/dscserver/{dsc_id}', 'GET', token)
