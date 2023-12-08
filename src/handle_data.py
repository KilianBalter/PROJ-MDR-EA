from ticket_037 import *


def handle_data(mdr_event: str) -> str:
    """method receives mdr event log as a python dictionary and
    returns the attacked system IPv6 address as a unique identifier"""

    sys_name = mdr_get_sys_name(mdr_event)

    return sys_name
