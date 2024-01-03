from src.ea_rest_template import ea_rest_call


def add_mitigation_status(token, event, satisfied_mitigations, unsatisfied_mitigations, error_message=""):
    # If EA reachable, get rule titles and add them as additional info
    if token:
        add_rule_titles(satisfied_mitigations, token)
        add_rule_titles(unsatisfied_mitigations, token)

    # Determine vulnerability status
    vuln_status = "NOT_VULNERABLE" if satisfied_mitigations else "VULNERABLE"

    # Add information to event
    event.update({
        "hardening_info": {
            # Mitigations for which all mapped rules are (not) present on the system
            # including descriptions for each mitigation and rule
            "satisfied_mitigations": satisfied_mitigations,
            "unsatisfied_mitigations": unsatisfied_mitigations,

            # Estimated vulnerability of the system
            "vulnerability_status": vuln_status,

            # Additional information about errors that occurred during lookup
            "error_message": error_message
        }
    })


def add_rule_titles(mitigations, token):
    if not mitigations:
        return

    updated_rules = {}
    for mitigation in mitigations:
        for rule in mitigations[mitigation]['rules']:
            response = ea_rest_call(f'/api/v3/benchmarkengine/Rules/{rule}', 'GET', token)
            updated_rules.update({
                rule: {
                    'title': response['title']
                }
            })

        mitigations[mitigation].update({
            "rules": updated_rules
        })
