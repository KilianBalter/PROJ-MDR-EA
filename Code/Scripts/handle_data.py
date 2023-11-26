import json
import logging
import re


def handle_data(mdr_event: str) -> str:
    """method receives mdr event log as a python dictionary and
    returns the attacked system IPv6 address as a unique identifier"""
    system_ipv6 = None
    try:
        system_ipv6 = mdr_event['event']['taxonomy']['External']['Attack']['victim']['machine']\
            ['Local']['host']['ip'][0]
    except KeyError:
        logging.error("Error in key path. Compare path in json file and in variable declaration!")
    except IndexError:
        logging.error("Error retrieving entry from selected path. Check entry in json file!")
    except json.decoder.JSONDecodeError:
        logging.error("Error in json file. Check for correct json syntax!")

    # checks validity of result with a regular expression
    assert re.match("^([0-9a-f]{0,4}:){2,8}[0-9a-f]{1,4}$", system_ipv6) is not None, "Invalid IPv6 syntax"

    return system_ipv6
