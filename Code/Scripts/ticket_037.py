import json
import logging


def mdr_get_sys_name(mdr_event: str) -> str:
    """
    returns the name of the attacked system
    """
    sys_name = None
    try:
        sys_name = mdr_event['event']['taxonomy']['External']['subject']['machine']['Local']\
            ['host']['name']
    except KeyError:
        logging.error("Error in key path. Compare path in json file and in variable declaration!")
    except json.decoder.JSONDecodeError:
        logging.error("Error in JSON file. Check for correct JSON syntax!")

    return sys_name
