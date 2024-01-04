from src.ea_rest_template import ea_rest_call


def update_mitigation_status(event, token, satisfied_mitigations=None, unsatisfied_mitigations=None, error_message=None):
    # If EA reachable, get rule titles and add them as additional info
    if token:
        add_rule_titles(satisfied_mitigations, token)
        add_rule_titles(unsatisfied_mitigations, token)

    # Reevaluate vulnerability status if satisfied mitigations is being updated
    vuln_status = None
    if satisfied_mitigations is not None:
        vuln_status = "NOT_VULNERABLE" if satisfied_mitigations else "VULNERABLE"

    # Gather all fields to be updated
    updated_fields = {}

    # Estimated vulnerability of the system
    if vuln_status is not None:
        updated_fields.update({
            "vulnerability_status": vuln_status
        })

    # Mitigations for which all mapped rules are (not) present on the system
    # including descriptions for each mitigation and rule
    if satisfied_mitigations is not None:
        updated_fields.update({
            "satisfied_mitigations": satisfied_mitigations
        })
    if unsatisfied_mitigations is not None:
        updated_fields.update({
            "unsatisfied_mitigations": unsatisfied_mitigations
        })

    # Additional information about errors that occurred during lookup
    if error_message is not None:
        updated_fields.update({
            "error_message": error_message
        })

    # Update fields in event
    event.update({
        "hardening_info": updated_fields
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
