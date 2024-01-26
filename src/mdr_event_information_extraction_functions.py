import logging


# Returns the name of the attacked system
def get_mdr_sys_name(mdr_event) -> str:
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
