from src.ea_rest_template import ea_rest_call


def update_mitigation_status(event, token=None, satisfied_mitigations=None, unsatisfied_mitigations=None,
                             error_message=None):
    # If EA reachable, get rule titles and add them as additional info
    if token:
        try:
            add_rule_titles(satisfied_mitigations, token)
            add_rule_titles(unsatisfied_mitigations, token)
        # Titles serve only as additional information. If anything goes wrong due to EA, ignore and just update fields
        except Exception:
            pass

    # Reevaluate vulnerability status if satisfied mitigations is being updated
    vuln_status = None
    if satisfied_mitigations is not None:
        vuln_status = "NOT_VULNERABLE" if satisfied_mitigations else "VULNERABLE"

    # Update fields
    # Estimated vulnerability of the system
    if vuln_status is not None:
        event["hardening_info"]['vulnerability_status'] = vuln_status

    # Mitigations for which (not) all mapped rules are present on the system,
    # including descriptions for each mitigation and rule
    if satisfied_mitigations is not None:
        event["hardening_info"]['satisfied_mitigations'] = satisfied_mitigations
    if unsatisfied_mitigations is not None:
        event["hardening_info"]['unsatisfied_mitigations'] = unsatisfied_mitigations

    # Additional information about errors that occurred during lookup
    if error_message is not None:
        event["hardening_info"]['error_message'] = error_message


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
