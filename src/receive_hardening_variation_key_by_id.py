from src.ea_rest_template import ea_rest_call


# main function
def get_hardening_variation_key_by_id(token: str, server_id: str) -> str:
    if not server_id:
        return ''

    try:
        dsc_server_id = get_dsc_server_id(token, server_id)
        dsc_server_application = get_dsc_server_application(token, dsc_server_id)
        for dsc in dsc_server_application:
            return dsc["variationKey"]
    except Exception:
        raise Exception("Error while retrieving hardening variation key by ID. Make sure variation key exists, and system is reachable.")


# Function to receive the dscServerId
def get_dsc_server_id(token, id_1):
    try:
        response = ea_rest_call(f'/api/dtools/DscServer/{id_1}', 'GET', token)
        return response["serverId"]
    except Exception:
        raise Exception("Error while retrieving dsc system id. make sure microservice dTools is running.")


# Function to receive the application information. Variation key is part of it
def get_dsc_server_application(token, dsc_id):
    try:
        return ea_rest_call(f'/api/dtools/DscServerApplication/dscserver/{dsc_id}', 'GET', token)
    except Exception:
        raise Exception("Error while retrieving the dsc server application. Make sure the dsc id is correct and icroservice dTools is running.")
