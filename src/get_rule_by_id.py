import requests
import json
from src.ea_rest_template import ea_rest_call


def get_rule_by_instance_name(token, instance_name):
    data = {'instanceNames': [instance_name]}
    response = ea_rest_call(f'/api/v3/hardeningengine/HardeningDsc/instanceRules', 'POST',  token, None, data)
    return get_rule_by_rule_id(token, json.dumps(response['resolvedRules'][0]['includedBy'][0]['ruleId']))


def get_rule_by_rule_id(token: str, rule_id: str):
    response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/'+rule_id, 'GET',  token, None)
    return json.dumps(response['settings'][0])
