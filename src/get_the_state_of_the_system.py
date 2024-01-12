from src.ea_rest_template import ea_rest_call
import json


# main function
def get_the_state(token: str, server_id: str) -> str:
    try:
        if not server_id:
            return ''
        # extract dscServerId
        response = ea_rest_call(f'/api/dtools/DscServer/{server_id}', 'GET', token)
        dsc_server_id = response["serverId"]
        # use dscServerId to get the ApplicationStatus
        response2 = ea_rest_call(f'/api/jobProcessing/DscServerApplicationStatus/dscserver/{dsc_server_id}', 'GET', token)
        # extract state_information and change the JSON-string to a python-dictionary
        state_information = json.loads(response2[0]['stateDetails'])
    except Exception:
        raise Exception("error in get_the_state")
    return state_information['InState']
