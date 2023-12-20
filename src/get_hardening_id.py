from src.ea_rest_template import ea_rest_call


def get_hardening_id(token, variation_key):
    hardening_info = ea_rest_call(f"/api/v3/benchmarkengine/HardeningDsc/config/{variation_key}/hardening",
                                  'POST', token)

    return hardening_info['id']
