from eaRestTemplate import ea_rest_call


# Retrieve all systems accessible in the EA
def get_all_systems(token: str):
    return ea_rest_call("/api/ibase/Server", 'GET', token)
