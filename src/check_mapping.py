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
