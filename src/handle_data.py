from my_credentials import get_credentials
from obtain_a_JWT_token import get_jwt_token
from ticket_037 import mdr_get_sys_name
from receive_list_of_systems_from_ea import get_all_systems
from extract_ea_system_id import get_ea_system_id_from_list_of_systems
from receive_hardening_variation_key_by_id import get_hardening_variation_key_by_id


def handle_data(event):
    vulnerable = True

    credentials = get_credentials()
    token = get_jwt_token(credentials['username'], credentials['password'])
    mdr_name = mdr_get_sys_name(event)
    servers = get_all_systems(token)
    ea_id = get_ea_system_id_from_list_of_systems(servers, mdr_name)
    variation_key = get_hardening_variation_key_by_id(token, ea_id)
    print(variation_key)

    return event, vulnerable
