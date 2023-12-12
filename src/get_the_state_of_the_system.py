from src.ea_rest_template import ea_rest_call


# main function
def get_the_state(token: str, server_id: str) -> str:
    if not server_id:
        return ''
    response = ea_rest_call(f'/api/dtools/DscServer/{server_id}', 'GET', token)
    return response["status"]



