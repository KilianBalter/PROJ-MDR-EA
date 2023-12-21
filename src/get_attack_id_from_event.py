import logging


def get_attack_id(mdr_event) -> str:  # Returns the attackId from the MDR event
    attack_id = None
    try:
        attack_id = mdr_event['event']['action']['details']['technique']['id']
    except KeyError:
        logging.error("Error in key path. Compare path in the JSON file and in variable declaration!")
    return attack_id
