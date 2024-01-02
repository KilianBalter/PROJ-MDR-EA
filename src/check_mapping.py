import json


def check_mapping(attack_id, rule_ids):
    with open("../assets/mapping.json", 'r') as f:
        mapping = json.load(f)
        satisfied_mitigations = []
        try:
            mitigations = mapping['techniques'][f'{attack_id}']['mitigations']

            for mitigation in mitigations:
                rules = mitigations[mitigation]['rules']
                if all(_id in rule_ids for _id in rules):
                    satisfied_mitigations.append(mitigation)
        except KeyError:  # Technique has not been mapped
            # Simply return empty satisfied_mitigations array
            pass

        return satisfied_mitigations
