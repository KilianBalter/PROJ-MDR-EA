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
        mapped_rules = mitigations[mitigation_id]['rules']

        # Sort rules into present and not present
        rules_present = [_id for _id in mapped_rules if _id in rule_ids]
        rules_not_present = [_id for _id in mapped_rules if _id not in rule_ids]

        # Update mitigation with that information
        updated_mitigation = mitigations[mitigation_id].copy()
        updated_mitigation['rules'] = {
            'present': rules_present,
            'not_present': rules_not_present
        }

        # ALL rules in mitigation are present
        if rules_present and not rules_not_present:
            if not partial:
                satisfied_mitigations[mitigation_id] = updated_mitigation
            else:
                partial_mitigations[mitigation_id] = updated_mitigation
        # SOME rules in mitigation are present
        elif rules_present and rules_not_present:
            partial_mitigations[mitigation_id] = updated_mitigation
        # NO rules in mitigation are present
        elif not rules_present and rules_not_present:
            unsatisfied_mitigations[mitigation_id] = updated_mitigation
        # There are no rule present or not present, meaning no rules were mapped to the mitigation at all
        else:
            raise Exception(f'No rule(s) mapped for mitigation {mitigation_id}')

    if not satisfied_mitigations and not partial_mitigations and not unsatisfied_mitigations:
        raise ValueError("No mitigations found in the mapping.")

    return satisfied_mitigations, partial_mitigations, unsatisfied_mitigations
