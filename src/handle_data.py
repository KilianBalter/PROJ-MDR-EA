import json

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
from src.check_mapping import check_mapping
from src.update_mitigation_status import update_mitigation_status


def handle_data(event):
    # Check if hardening info field already exists -> event has already been processed
    if 'hardening_info' in event.keys():
        return event
    # If field doesn't exist, initialize with default values and continue processing
    else:
        event.update({
            "hardening_info": {
                # Mitigations for which all mapped rules are (not) present on the system
                # including descriptions for each mitigation and rule
                "satisfied_mitigations": {},
                "partial_mitigations": {},
                "unsatisfied_mitigations": {},

                # Estimated vulnerability of the system
                "vulnerability_status": "VULNERABLE",

                # Additional information about errors that occurred during lookup
                "error_message": None
            }
        })

    # Initialize variables
    token = None
    satisfied_mitigations = None
    partial_mitigations = None
    unsatisfied_mitigations = None
    error_message = None

    try:
        # Check if technique has been mapped and get mitigations
        attack_id = get_attack_id(event)
        with open("../assets/mapping.json", 'r') as f:
            mapping = json.load(f)
            if attack_id not in mapping['techniques']:
                update_mitigation_status(event, error_message=f"Technique {attack_id} has not been mapped")
                return event

            mitigations = mapping['techniques'][f'{attack_id}']['mitigations']

        # EA
        # Credentials
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])

        # Add all mitigations as unsatisfied by default in case an error is encountered during processing
        update_mitigation_status(event, token=token, unsatisfied_mitigations=mitigations)

        # Get EA system ID for this system
        mdr_name = get_mdr_sys_name(event)
        systems = get_all_systems(token)
        ea_system_id = get_ea_system_id_from_list_of_systems(systems, mdr_name)

        # Check whether system is InState
        state = get_the_state(token, ea_system_id)
        if not state:
            update_mitigation_status(event, error_message="System is not in state")
            return event

        # Get all hardening rules applied on this system
        variation_key = get_hardening_variation_key_by_id(token, ea_system_id)
        hardening_id = get_hardening_id(token, variation_key)
        rules = get_rule_ids(token, hardening_id)

        # Check mapping for which mitigations are (not/partially) satisfied
        satisfied_mitigations, partial_mitigations, unsatisfied_mitigations = check_mapping(mitigations, rules)

    # Catch any exception and save its message to include in the output event
    except Exception as e:
        if e.args:
            error_message = e.args[0]

    # Update event with gathered information
    update_mitigation_status(event, token, satisfied_mitigations, partial_mitigations, unsatisfied_mitigations,
                             error_message)

    return event
