import json


def check_mapping(attack_id, rule_ids):
    with open("../assets/mapping.json", 'r') as f:
        mapping = json.load(f)
        if attack_id not in mapping['techniques']:
            raise LookupError(f"Technique {attack_id} has not been mapped")

        satisfied_mitigations = {}
        unsatisfied_mitigations = {}
        mitigations = mapping['techniques'][f'{attack_id}']['mitigations']

        for mitigation_id in mitigations:
            rules = mitigations[mitigation_id]['rules']
            if all(_id in rule_ids for _id in rules):
                satisfied_mitigations.update({mitigation_id: mitigations[mitigation_id]})
            else:
                unsatisfied_mitigations.update({mitigation_id: mitigations[mitigation_id]})

        return satisfied_mitigations, unsatisfied_mitigations
