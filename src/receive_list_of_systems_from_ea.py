from src.ea_rest_template import ea_rest_call


# Retrieve all systems accessible in the EA
def get_all_systems(token: str):
    try:
        return ea_rest_call("/api/ibase/Server", 'GET', token)
    except Exception:
        raise Exception("Could not get all systems. Make sure microservice iBase is running.")