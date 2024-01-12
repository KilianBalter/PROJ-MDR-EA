import json

from src.ea_rest_template import ea_rest_call


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
        raise Exception("error in get_rule_by_instance_name")


def get_rule_by_rule_id(token: str, rule_id: str):
    try:
        response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/' + rule_id, 'GET', token, None)
    except Exception:
        raise Exception("error in get_rule_by_rule_id")
    return json.dumps(response['settings'][0])
