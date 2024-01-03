from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.get_mdr_name_from_event import get_mdr_sys_name
from src.get_attack_id_from_event import get_attack_id
from src.receive_list_of_systems_from_ea import get_all_systems
from src.extract_ea_system_id import get_ea_system_id_from_list_of_systems
from src.receive_hardening_variation_key_by_id import get_hardening_variation_key_by_id
from src.get_hardening_id import get_hardening_id
from src.get_rule_ids import get_rule_ids
from src.get_the_state_of_the_system import get_the_state
from check_mapping import check_mapping
from add_mitigation_status import add_mitigation_status


def handle_data(event):
    # Check if hardening info field already exists -> event has already been processed
    try:
        if event['hardening_info']:
            return event
    # If field doesn't exist, continue processing
    except KeyError:
        pass

    token = None
    satisfied_mitigations = None
    unsatisfied_mitigations = None
    error_message = None

    try:
        # Credentials
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])

        # Get information from event
        mdr_name = get_mdr_sys_name(event)
        attack_id = get_attack_id(event)

        # Get EA system ID for this system
        systems = get_all_systems(token)
        ea_system_id = get_ea_system_id_from_list_of_systems(systems, mdr_name)

        # Check whether system is InState
        state = get_the_state(token, ea_system_id)
        if not state:
            add_mitigation_status(token, event, satisfied_mitigations, unsatisfied_mitigations, "System is not in state")
            return event

        # Get all hardening rules applied on this system
        variation_key = get_hardening_variation_key_by_id(token, ea_system_id)
        hardening_id = get_hardening_id(token, variation_key)
        rules = get_rule_ids(token, hardening_id)

        # Check mapping for which mitigations are satisfied
        satisfied_mitigations, unsatisfied_mitigations = check_mapping(attack_id, rules)

    # Catch any exception and save its message to include in the output event
    except LookupError as e:
        if e.args:
            error_message = e.args[0]
    except Exception as e:
        if e.args:
            error_message = e.args[0]

    # Add gathered information to input event
    add_mitigation_status(token, event, satisfied_mitigations, unsatisfied_mitigations, error_message)

    return event
