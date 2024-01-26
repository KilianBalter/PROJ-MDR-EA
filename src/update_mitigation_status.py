from src.ea_rest_template import ea_rest_call


def update_mitigation_status(event, token=None, satisfied_mitigations=None, partial_mitigations=None,
                             unsatisfied_mitigations=None, error_message=None):
    try:
        _satisfied_mitigations = None
        _partial_mitigations = None
        _unsatisfied_mitigations = None

        # Copy dicts
        if satisfied_mitigations is not None:
            _satisfied_mitigations = satisfied_mitigations.copy()
        if partial_mitigations is not None:
            _partial_mitigations = partial_mitigations.copy()
        if unsatisfied_mitigations is not None:
            _unsatisfied_mitigations = unsatisfied_mitigations.copy()

        # If EA reachable, get rule titles and add them as additional info
        if token:
            try:
                add_rule_titles(satisfied_mitigations, False, token)
                add_rule_titles(partial_mitigations, True, token)
                add_rule_titles(unsatisfied_mitigations, False, token)
            # Titles serve only as additional information. If anything goes wrong due to EA, ignore and just update fields
            except Exception:
                pass

        # Update fields
        # Mitigations for which all/some/none mapped rules are present on the system,
        # including descriptions for each mitigation and rule
        if _satisfied_mitigations is not None:
            event["hardening_info"]['satisfied_mitigations'] = _satisfied_mitigations
        if _partial_mitigations is not None:
            event["hardening_info"]['partial_mitigations'] = _partial_mitigations
        if _unsatisfied_mitigations is not None:
            event["hardening_info"]['unsatisfied_mitigations'] = _unsatisfied_mitigations

        # Reevaluate vulnerability status
        if event["hardening_info"]['satisfied_mitigations']:
            vuln_status = "NOT_VULNERABLE"
        elif event["hardening_info"]['partial_mitigations']:
            vuln_status = "PARTIALLY_VULNERABLE"
        else:
            vuln_status = "VULNERABLE"
        # Estimated vulnerability of the system
        event["hardening_info"]['vulnerability_status'] = vuln_status

        # Additional information about errors that occurred during lookup
        if error_message is not None:
            event["hardening_info"]['error_message'] = error_message
    except Exception:
        raise Exception("Error while updating the mitigation status. Input information might be missing, check the parameter inputs.")


def add_rule_titles(mitigations, partial, token):
    try:
        if not mitigations:
            return

        if partial:
            updated_rules = {
                'present': {},
                'not_present': {}
            }
            for mitigation in mitigations:
                for rule in mitigations[mitigation]['rules']['present']:
                    updated_rules['present'][rule] = {'title': get_rule_title(rule, token)}
                for rule in mitigations[mitigation]['rules']['not_present']:
                    updated_rules['not_present'][rule] = {'title': get_rule_title(rule, token)}
                mitigations[mitigation]['rules'] = updated_rules
        else:
            updated_rules = {}
            for mitigation in mitigations:
                for rule in mitigations[mitigation]['rules']:
                    updated_rules[rule] = {'title': get_rule_title(rule, token)}
                mitigations[mitigation]['rules'] = updated_rules
    except Exception:
        raise Exception("Error while adding rule titles. Make sure microservice BenchmarkEngine is running.")


def get_rule_title(rule, token):
    response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/{rule}', 'GET', token)
    return response['title']


# Logic for whether a mitigation is considered satisfied, partial, or unsatisfied
# "Partial" refers to the value of the "partial" field in the mapping for that mitigation
# -------------------------------------------
# | Partial | Rules present | Result        |
# |  False  |      ALL      |  SATISFIED    |
# |  False  |      SOME     |  PARTIAL      |
# |  False  |      NONE     |  UNSATISFIED  |
# |  True   |      ALL      |  PARTIAL      |
# |  True   |      SOME     |  PARTIAL      |
# |  True   |      NONE     |  UNSATISFIED  |
# -------------------------------------------
def check_mapping(mitigations, rule_ids):
    satisfied_mitigations = {}
    partial_mitigations = {}
    unsatisfied_mitigations = {}

    for mitigation_id in mitigations:
        partial = mitigations[mitigation_id]['partial']
        rules = mitigations[mitigation_id]['rules']

        # ALL rules in mitigation are present
        if all(_id in rule_ids for _id in rules):
            # Add mitigation to dict (partial_mitigations if it is tagged partial)
            if partial:
                partial_mitigations[mitigation_id] = mitigations[mitigation_id]
            else:
                satisfied_mitigations[mitigation_id] = mitigations[mitigation_id]

        # ANY rule in mitigation is present
        elif any(_id in rule_ids for _id in rules):
            # Separate rules that are present/not present
            rules_present = [_id in rule_ids for _id in rules]
            rules_not_present = [_id not in rule_ids for _id in rules]

            # Add mitigation to dict
            partial_mitigations[mitigation_id] = mitigations[mitigation_id]

            # Update 'rules' field with separated lists
            partial_mitigations[mitigation_id]['rules'] = {
                "present": rules_present,
                "not_present": rules_not_present
            }

        # NO rule in mitigation is present
        else:
            # Add mitigation to dict
            unsatisfied_mitigations[mitigation_id] = mitigations[mitigation_id]

    if not satisfied_mitigations and not partial_mitigations and not unsatisfied_mitigations:
        raise ValueError("No mitigations found in the mapping.")

    return satisfied_mitigations, partial_mitigations, unsatisfied_mitigations
