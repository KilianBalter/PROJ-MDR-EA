import json

from my_credentials import get_credentials
from obtain_a_JWT_token import get_jwt_token
from receive_list_of_systems_from_ea import get_list_of_systems_from_ea
from extract_ea_system_id import get_ea_system_id_from_list_of_systems
from receive_hardening_variation_key_by_id import get_hardening_variation_key_by_id


# Extract MDR name from an event
def get_mdr_name_from_event(mdr_event) -> str:
    if not mdr_event:
        return ''
    return mdr_event['event']['taxonomy']['External']['subject']['machine']['Local']['host']['name']


def handle_data(event):
    vulnerable = True

    credentials = get_credentials()
    token = get_jwt_token(credentials['username'], credentials['password'])
    mdr_name = get_mdr_name_from_event(event)
    servers = get_list_of_systems_from_ea(token)
    ea_id = get_ea_system_id_from_list_of_systems(servers, mdr_name)
    variation_key = get_hardening_variation_key_by_id(token, ea_id)
    print(variation_key)

    return event, vulnerable


if __name__ == "__main__":
    with open("../assets/Test_Event_1.json") as event_file:
        event = json.load(event_file)
        handle_data(event)
