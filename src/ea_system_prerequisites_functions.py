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
        # in case response is empty
        if not response2:
            raise Exception("Error while retrieving the state of the system. State of system is empty. Make sure the hardening has been applied and not just assigned.")
        # extract state_information and change the JSON-string to a python-dictionary
        state_information = json.loads(response2[0]['stateDetails'])
    except Exception:
        raise Exception("Error while retrieving the state of the system. Make sure the ID of the system exists and hardening has been applied, microservices dTools and dTools.jobProcessing are running.")
    return state_information['InState']
