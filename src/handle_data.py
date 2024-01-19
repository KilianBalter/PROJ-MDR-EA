import json
import requests
import logging
import re

from my_credentials import get_credentials


# vvvvvvvvvvvvvvvv UNUSED vvvvvvvvvvvvvvvv
def get_rule_by_instance_name(token, instance_name):
    try:
        if isinstance(instance_name, list):
            data = {'instanceNames': instance_name}
        else:
            data = {'instanceNames': [instance_name]}
        response = ea_rest_call(f'/api/v3/hardeningengine/HardeningDsc/instanceRules', 'POST', token, None, data)
        for i in range(len(response['resolvedRules'])):
            return get_rule_by_rule_id(token, json.dumps(response['resolvedRules'][i]['includedBy'][0]['ruleId']))
    except Exception:
        raise Exception("Error while retrieving rule by instance name. Make sure rule and instance name are accessible and microservice HardeningEngine is running.")


def get_rule_by_rule_id(token: str, rule_id: str):
    try:
        response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/' + rule_id, 'GET', token, None)
    except Exception:
        raise Exception("Error while retrieving rule by rule id. Make sure the rule id is correct and microservice BenchmarkEngine is running.")
    return json.dumps(response['settings'][0])


def receive_instance_name(code_template: str) -> str | list[str]:
    """
    this function receives the code_template and filters it for all xRegistry instance_names
    :param code_template:
    :return: empty String if there is no code_template, list of instance_names in the code_template otherwise
    """
    try:
        if not code_template:
            return ''
        lines = code_template.splitlines()
        # filtering the lines to only work with the lines that contain xRegistry
        x_reg = [x for x in lines if "xRegistry" in x]
        # converting the array into a single string so that
        x_reg_str = ''.join(x_reg)
        return find_all_instance_names(x_reg_str)
    except Exception:
        raise Exception("Error in receiving instance name. The code_template might have changed, analysis of code is required.")


def find_all_instance_names(text: str) -> list[str]:
    """
    this function filters a String for every instance name with a RegEx
    """
    pattern = r'[A-Z0-9]{23,24}'
    try:
        return [match.group() for match in re.finditer(pattern, text)]
    except Exception:
        raise Exception("Error in finding instance names within regex text. Make sure the injected string has been extracted correctly, analysis of code is required.")
# ^^^^^^^^^^^^^^^^ UNUSED ^^^^^^^^^^^^^^^^


def get_jwt_token(username: str, password: str):
    url = "http://win-jtn7m3lf4bq.theagleenforce.local:5000/api/logon/LoginForms"

    # Define the headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    # Define the data for the request
    body = {
        'username': username,
        'password': password
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=body)

    response.raise_for_status()

    return response.json().get('token')


# Function to make an API-Call to the EA
def ea_rest_call(endpoint: str, methodtype: str, token: str, params=None, _json=None):
    url = 'http://win-jtn7m3lf4bq.theagleenforce.local:5000' + endpoint
    credentials = 'Bearer ' + token

    headers = {
        'Nfclient': 'nftestapi',
        'Content-Type': 'application/json',
        'Authorization': credentials
    }

    response = requests.request(methodtype, url, headers=headers, params=params, json=_json)

    response.raise_for_status()

    data = response.json()
    return data


# Returns the name of the attacked system
def get_mdr_sys_name(mdr_event):
    sys_name = None
    try:
        sys_name = mdr_event['event']['taxonomy']['External']['subject']['machine']['Local']['host']['name']
    except KeyError:
        logging.error("Error in key path. Compare path in json file and in variable declaration!")
        raise

    return sys_name


def get_attack_id(mdr_event) -> str:  # Returns the attackId from the MDR event
    attack_id = None
    try:
        attack_id = mdr_event['event']['taxonomy']['External']['Attack']['action']['details']['technique']['id']
    except KeyError:
        logging.error("Error in key path. Compare path in the JSON file and in variable declaration!")
        raise

    return attack_id


# Retrieve all systems accessible in the EA
def get_all_systems(token: str):
    try:
        return ea_rest_call("/api/ibase/Server", 'GET', token)
    except Exception:
        raise Exception("Could not get all systems. Make sure microservice iBase is running.")


def get_ea_system_id_from_list_of_systems(server_list, mdr_name: str) -> str:
    # Check if either server_list or mdr_name is None or '', and return '' if true
    if not server_list:
        raise ValueError("EA server list is empty")
    if not mdr_name:
        raise ValueError("System name couldn't be found in event")

    system_id = None

    # Iterate through the server_list
    for server in server_list:
        # Check if the lowercase name of the current server matches the lowercase mdr_name
        if server['name'].lower() == mdr_name.lower():
            # Return the ID of the matching server
            system_id = str(server['id'])

    if system_id is None:
        raise Exception("System not found in EA server list")

    return system_id


def get_hardening_variation_key_by_id(token: str, server_id: str) -> str:
    if not server_id:
        raise Exception("Error while retrieving hardening variation key by ID. The system id has not been passed, make sure it is passed correctly.")

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


def get_hardening_id(token, variation_key):
    # Better call. Leaving here in case it works in the future
    # hardening_info = ea_rest_call(f"/api/v3/benchmarkengine/HardeningDsc/config/{variation_key}/hardening",
    #                               'POST', token)
    #
    # return hardening_info['id']

    # Get all configuration templates
    try:
        templates = ea_rest_call('/api/dtools/DscApplicationConfigTemplate', 'GET', token)
    except Exception:
        raise Exception("Error in retrieving configuration template. Make sure configuration templates exist and the microservice dTools is running.")

    # Search for template corresponding to given variation key
    template_id = None
    i = 0
    while template_id is None and i < len(templates):
        if templates[i]['variationKey'] == variation_key:
            template_id = templates[i]['id']
        i += 1

    # Get hardening ID from corresponding template
    try:
        conf_template = ea_rest_call(f"/api/dtools/DscApplicationConfigTemplate/{template_id}", 'GET', token)
    except Exception:
        raise Exception(
            "Error while retrieving hardening configuration template by ID. Make sure microservice dTools is running and ID of configuration template exists.")

    data_template = json.loads(conf_template['dataTemplate'])  # json.loads() because the dataTemplate field is a string
    hardening_id = data_template['hardeningId']

    return hardening_id


# Retrieves list of IDs of all rules contained in a Hardening
def get_rule_ids(token, hardening_id) -> list[int]:
    try:
        # Get information about the specific hardening (included benchmarks, excluded rules, etc...)
        hardening_info = ea_rest_call(f"/api/v3/hardeningengine/Hardenings/{hardening_id}", "GET", token)

        # Filter the response to only benchmarks and excluded rules for the HardeningWizard
        keys = ['includes', 'conflictExcludes', 'gpoExcludes', 'manualExcludes']
        wizard_body = {key: hardening_info[key] for key in keys}

        # Append some additional required fields
        # Just assigning pageSize a very big value to get all rules every time
        wizard_body.update({
            'benchmarkId': None,
            'onlyExcluded': False,
            'pageSize': 1_000_000,
            'refIdFilter': None,
            'startIndex': 0,
            'titleFilter': None})

        # Retrieve rule information from the HardeningWizard
        rules = ea_rest_call("/api/v3/hardeningengine/HardeningWizard/rules", 'POST', token, _json=wizard_body)

        # Get only excluded rules to filter them out later
        wizard_body.update({
            'onlyExcluded': True
        })

        excluded_rules = ea_rest_call("/api/v3/hardeningengine/HardeningWizard/rules",
                                      'POST', token, _json=wizard_body)

        # Filter out only the rule IDs
        all_rule_ids = [rule['includedBy'][0]['ruleId'] for rule in rules['items']]
        excluded_rule_ids = [rule['includedBy'][0]['ruleId'] for rule in excluded_rules['items']]

        # Filter out excluded rules
        rule_ids = [rule_id for rule_id in all_rule_ids if rule_id not in excluded_rule_ids]
    except Exception:
        raise Exception("Error while retrieving IDs of all rules. Make sure the microservice HardeningEngine is running.")
    return rule_ids


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


# Logic for whether a mitigation is considered satisfied, partial, or unsatisfied
# "Partial" refers to the value of the "partial" field in the mapping for that mitigation
# -------------------------------------------
# | Partial | Rules present | Result        |
# |  False  |      ALL      |  SATISFIED    |
# |  False  |      SOME     |  PARTIAL      |
# |  False  |      NONE     |  UNSATISFIED  |
# |  True   |      ALL      |  PARTIAL      |
# |  True   |      SOME     |  PARTIAL      |
# |  True   |      NONE     |  UNSATISFIED  |
# -------------------------------------------
def check_mapping(mitigations, rule_ids):
    satisfied_mitigations = {}
    partial_mitigations = {}
    unsatisfied_mitigations = {}

    for mitigation_id in mitigations:
        partial = mitigations[mitigation_id]['partial']
        mapped_rules = mitigations[mitigation_id]['rules']

        # Sort rules into present and not present
        rules_present = [_id for _id in mapped_rules if _id in rule_ids]
        rules_not_present = [_id for _id in mapped_rules if _id not in rule_ids]

        # Update mitigation with that information
        updated_mitigation = mitigations[mitigation_id].copy()
        updated_mitigation['rules'] = {
            'present': rules_present,
            'not_present': rules_not_present
        }

        # ALL rules in mitigation are present
        if rules_present and not rules_not_present:
            if not partial:
                satisfied_mitigations[mitigation_id] = updated_mitigation
            else:
                partial_mitigations[mitigation_id] = updated_mitigation
        # SOME rules in mitigation are present
        elif rules_present and rules_not_present:
            partial_mitigations[mitigation_id] = updated_mitigation
        # NO rules in mitigation are present
        elif not rules_present and rules_not_present:
            unsatisfied_mitigations[mitigation_id] = updated_mitigation
        # There are no rule present or not present, meaning no rules were mapped to the mitigation at all
        else:
            raise Exception(f'No rule(s) mapped for mitigation {mitigation_id}')

    if not satisfied_mitigations and not partial_mitigations and not unsatisfied_mitigations:
        raise ValueError("No mitigations found in the mapping.")

    return satisfied_mitigations, partial_mitigations, unsatisfied_mitigations


def update_mitigation_status(event, token=None, satisfied_mitigations=None, partial_mitigations=None,
                             unsatisfied_mitigations=None, error_message=None):
    try:
        _satisfied_mitigations = None
        _partial_mitigations = None
        _unsatisfied_mitigations = None

        # Copy dicts
        if satisfied_mitigations is not None:
            _satisfied_mitigations = satisfied_mitigations.copy()
        if partial_mitigations is not None:
            _partial_mitigations = partial_mitigations.copy()
        if unsatisfied_mitigations is not None:
            _unsatisfied_mitigations = unsatisfied_mitigations.copy()

        # If EA reachable, get rule titles and add them as additional info
        if token:
            try:
                add_rule_titles(satisfied_mitigations, token)
                add_rule_titles(partial_mitigations, token)
                add_rule_titles(unsatisfied_mitigations, token)
            # Titles serve only as additional information.
            # If anything goes wrong due to EA, ignore and just update fields
            except Exception:
                pass

        # Update fields
        # Mitigations for which all/some/none mapped rules are present on the system,
        # including descriptions for each mitigation and rule
        if _satisfied_mitigations is not None:
            event["hardening_info"]['satisfied_mitigations'] = _satisfied_mitigations
        if _partial_mitigations is not None:
            event["hardening_info"]['partial_mitigations'] = _partial_mitigations
        if _unsatisfied_mitigations is not None:
            event["hardening_info"]['unsatisfied_mitigations'] = _unsatisfied_mitigations

        # Reevaluate vulnerability status
        if event["hardening_info"]['satisfied_mitigations']:
            vuln_status = "NOT_VULNERABLE"
        elif event["hardening_info"]['partial_mitigations']:
            vuln_status = "PARTIALLY_VULNERABLE"
        else:
            vuln_status = "VULNERABLE"
        # Estimated vulnerability of the system
        event["hardening_info"]['vulnerability_status'] = vuln_status

        # Additional information about errors that occurred during lookup
        if error_message is not None:
            event["hardening_info"]['error_message'] = error_message
    except Exception:
        raise Exception("Error while updating the mitigation status. Input information might be missing, check the parameter inputs.")


def add_rule_titles(mitigations, token):
    try:
        if not mitigations:
            return

        # Make new dict for rules, because each rule is now a key instead of an array value
        updated_rules = {
            'present': {},
            'not_present': {}
        }

        # Add each rule with its title
        for mitigation in mitigations:
            for rule in mitigations[mitigation]['rules']['present']:
                updated_rules['present'][rule] = {'title': get_rule_title(rule, token)}
            for rule in mitigations[mitigation]['rules']['not_present']:
                updated_rules['not_present'][rule] = {'title': get_rule_title(rule, token)}

            # Update mitigation with new rules dict
            mitigations[mitigation]['rules'] = updated_rules
    except Exception:
        raise Exception("Error while adding rule titles. Make sure microservice BenchmarkEngine is running.")


def get_rule_title(rule, token):
    response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/{rule}', 'GET', token)
    return response['title']


def handle_data(event):
    # Check if hardening info field already exists -> event has already been processed
    if 'hardening_info' in event.keys():
        return event
    # If field doesn't exist, initialize with default values and continue processing
    else:
        event.update({
            "hardening_info": {
                # Mitigations for which all mapped rules are (not) present on the system
                # including descriptions for each mitigation and rule
                "satisfied_mitigations": {},
                "partial_mitigations": {},
                "unsatisfied_mitigations": {},

                # Estimated vulnerability of the system
                "vulnerability_status": "VULNERABLE",

                # Additional information about errors that occurred during lookup
                "error_message": None
            }
        })

    # Initialize variables
    token = None
    satisfied_mitigations = None
    partial_mitigations = None
    unsatisfied_mitigations = None
    error_message = None

    try:
        # Check if technique has been mapped and get mitigations
        attack_id = get_attack_id(event)
        with open("../assets/mapping.json", 'r') as f:
            mapping = json.load(f)
            if attack_id not in mapping['techniques']:
                update_mitigation_status(event, error_message=f"Technique {attack_id} has not been mapped")
                return event

            mitigations = mapping['techniques'][f'{attack_id}']['mitigations']

        # EA
        # Credentials
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])

        # Add all mitigations as unsatisfied by default in case an error is encountered during processing
        satisfied_mitigations, partial_mitigations, unsatisfied_mitigations = check_mapping(mitigations, [])
        update_mitigation_status(event, token=token, unsatisfied_mitigations=unsatisfied_mitigations)

        # Get EA system ID for this system
        mdr_name = get_mdr_sys_name(event)
        systems = get_all_systems(token)
        ea_system_id = get_ea_system_id_from_list_of_systems(systems, mdr_name)

        # Check whether system is InState
        state = get_the_state(token, ea_system_id)
        if not state:
            update_mitigation_status(event, error_message="System is not in state")
            return event

        # Get all hardening rules applied on this system
        variation_key = get_hardening_variation_key_by_id(token, ea_system_id)
        hardening_id = get_hardening_id(token, variation_key)
        rules = get_rule_ids(token, hardening_id)

        # Check mapping for which mitigations are (not/partially) satisfied
        satisfied_mitigations, partial_mitigations, unsatisfied_mitigations = check_mapping(mitigations, rules)

    # Catch any exception and save its message to include in the output event
    except Exception as e:
        if e.args:
            error_message = e.args[0]

    # Update event with gathered information
    update_mitigation_status(event, token, satisfied_mitigations, partial_mitigations, unsatisfied_mitigations,
                             error_message)

    return event
