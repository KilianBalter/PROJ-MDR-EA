import json


def check_mapping(mitigations, rule_ids):
    satisfied_mitigations = {}
    unsatisfied_mitigations = {}

    for mitigation_id in mitigations:
        rules = mitigations[mitigation_id]['rules']
        if all(_id in rule_ids for _id in rules):
            satisfied_mitigations.update({mitigation_id: mitigations[mitigation_id]})
        else:
            unsatisfied_mitigations.update({mitigation_id: mitigations[mitigation_id]})

    return satisfied_mitigations, unsatisfied_mitigations
