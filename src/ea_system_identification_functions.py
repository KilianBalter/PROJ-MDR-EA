from src.ea_rest_template import ea_rest_call


# Retrieve all systems accessible in the EA
def get_all_systems(token: str):
    try:
        return ea_rest_call("/api/ibase/Server", 'GET', token)
    except Exception:
        raise Exception("Could not get all systems. Make sure microservice iBase is running.")


def get_ea_system_id_from_list_of_systems(server_list, mdr_name: str) -> str:
    # Check if either server_list or mdr_name is None or '', and return '' if true
    if not server_list or not mdr_name:
        return ''

    # Iterate through the server_list
    for server in server_list:
        # Check if the lowercase name of the current server matches the lowercase mdr_name
        if server['name'].lower() == mdr_name.lower():
            # Return the ID of the matching server
            return str(server['id'])

    # If no matching server is found, return ''
    return ''
