import logging


# Returns the name of the attacked system
def get_mdr_sys_name(mdr_event) -> str:
    sys_name = None
    try:
        sys_name = mdr_event['event']['taxonomy']['External']['subject']['machine']['Local']['host']['name']
    except KeyError:
        logging.error("Error in key path. Compare path in json file and in variable declaration!")

    return sys_name
