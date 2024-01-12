from src.ea_rest_template import ea_rest_call

import requests


def get_hardening_configuration_template_by_id(token, _id):
    try:
        return ea_rest_call(f"/api/dtools/DscApplicationConfigTemplate/{_id}", 'GET', token)
    except Exception:
        raise Exception("error in get_hardening_configuration_template_by_id")