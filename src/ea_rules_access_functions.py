import json

from src.ea_rest_template import ea_rest_call
from src.receive_hardening_configuration_by_id import get_hardening_configuration_template_by_id


# main function
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
    """
    hardening_info = ea_rest_call(f"/api/v3/benchmarkengine/HardeningDsc/config/{variation_key}/hardening",
                                  'POST', token)

    return hardening_info['id']
    """

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
        conf_template = get_hardening_configuration_template_by_id(token, template_id)
    except Exception:
        raise Exception("Error in retrieving specific configuration template. Make sure the ID of the configuration template exists.")
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
        rules = ea_rest_call("/api/v3/hardeningengine/HardeningWizard/rules", 'POST', token, data=wizard_body)

        # Get only excluded rules to filter them out later
        wizard_body.update({
            'onlyExcluded': True
        })

        excluded_rules = ea_rest_call("/api/v3/hardeningengine/HardeningWizard/rules",
                                      'POST', token, data=wizard_body)

        # Filter out only the rule IDs
        all_rule_ids = [rule['includedBy'][0]['ruleId'] for rule in rules['items']]
        excluded_rule_ids = [rule['includedBy'][0]['ruleId'] for rule in excluded_rules['items']]

        # Filter out excluded rules
        rule_ids = [rule_id for rule_id in all_rule_ids if rule_id not in excluded_rule_ids]
    except Exception:
        raise Exception("Error while retrieving IDs of all rules. Make sure the microservice HardeningEngine is running.")
    return rule_ids


def get_rule_by_instance_name(token, instance_name):
    try:
        if isinstance(instance_name, list):
            data = {'instanceNames': instance_name}
        else:
            data = {'instanceNames': [instance_name]}
        response = ea_rest_call(f'/api/v3/hardeningengine/HardeningDsc/instanceRules', 'POST', token, None, data)
        for i in range(len(response['resolvedRules'])):
            print(get_rule_by_rule_id(token, json.dumps(response['resolvedRules'][i]['includedBy'][0]['ruleId'])))
    except Exception:
        raise Exception("Error while retrieving rule by instance name. Make sure rule and instance name are accessible and microservice HardeningEngine is running.")


def get_rule_by_rule_id(token: str, rule_id: str):
    try:
        response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/' + rule_id, 'GET', token, None)
    except Exception:
        raise Exception("Error while retrieving rule by rule id. Make sure the rule id is correct and microservice BenchmarkEngine is running.")
    return json.dumps(response['settings'][0])
