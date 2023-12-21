import json

from src.ea_rest_template import ea_rest_call
from src.receive_hardening_configuration_by_id import get_hardening_configuration_template_by_id


def get_hardening_id(token, variation_key):
    # Better call. Leaving here in case it works in the future
    """
    hardening_info = ea_rest_call(f"/api/v3/benchmarkengine/HardeningDsc/config/{variation_key}/hardening",
                                  'POST', token)

    return hardening_info['id']
    """

    # Get all configuration templates
    templates = ea_rest_call('/api/dtools/DscApplicationConfigTemplate', 'GET', token)

    # Search for template corresponding to given variation key
    template_id = None
    for template in templates:
        if template['variationKey'] == variation_key:
            template_id = template['id']
            break

    # Get hardening ID from corresponding template
    conf_template = get_hardening_configuration_template_by_id(token, template_id)
    data_template = json.loads(conf_template['dataTemplate'])  # json.loads() because the dataTemplate field is a string
    hardening_id = data_template['hardeningId']

    return hardening_id