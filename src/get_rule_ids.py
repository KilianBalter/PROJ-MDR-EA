from src.ea_rest_template import ea_rest_call


# Retrieves list of IDs of all rules contained in a Hardening
def get_rule_ids(token, hardening_id) -> list[int]:
    try:
        # Get information about the specific hardening (included benchmarks, excluded rules, etc...)
        hardening_info = ea_rest_call(f"/api/v3/hardeningengine/Hardenings/{hardening_id}", "GET", token)

        # Filter the response to only benchmarks and excluded rules for the HardeningWizard
        keys = ['includes', 'conflictExcludes', 'gpoExcludes', 'manualExcludes']
        wizard_body = {key: hardening_info[key] for key in keys}

        # Append some additional required fields
        # Just assigning pageSize a very big value to get all rules every time
        wizard_body.update({
            'benchmarkId': None,
            'onlyExcluded': False,
            'pageSize': 1_000_000,
            'refIdFilter': None,
            'startIndex': 0,
            'titleFilter': None})

        # Retrieve rule information from the HardeningWizard
        rules = ea_rest_call("/api/v3/hardeningengine/HardeningWizard/rules", 'POST', token, data=wizard_body)

        # Get only excluded rules to filter them out later
        wizard_body.update({
            'onlyExcluded': True
        })

        excluded_rules = ea_rest_call("/api/v3/hardeningengine/HardeningWizard/rules",
                                      'POST', token, data=wizard_body)

        # Filter out only the rule IDs
        all_rule_ids = [rule['includedBy'][0]['ruleId'] for rule in rules['items']]
        excluded_rule_ids = [rule['includedBy'][0]['ruleId'] for rule in excluded_rules['items']]

        # Filter out excluded rules
        rule_ids = [rule_id for rule_id in all_rule_ids if rule_id not in excluded_rule_ids]
    except Exception:
        raise Exception("error in get_rule_ids")
    return rule_ids
