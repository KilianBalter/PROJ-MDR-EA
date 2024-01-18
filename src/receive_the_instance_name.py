import re


def receive_instance_name(code_template: str) -> str | list[str]:
    """
    this function receives the code_template and filters it for all xRegistry instance_names
    :param code_template:
    :return: empty String if there is no code_template, list of instance_names in the code_template otherwise
    """
    try:
        if not code_template:
            return ''
        lines = code_template.splitlines()
        # filtering the lines to only work with the lines that contain xRegistry
        x_reg = [x for x in lines if "xRegistry" in x]
        # converting the array into a single string so that
        x_reg_str = ''.join(x_reg)
        return find_all_instance_names(x_reg_str)
    except Exception:
        raise Exception("Error in receiving instance name. The code_template might have changed, analysis of code is required.")


def find_all_instance_names(text: str) -> list[str]:
    """
    this function filters a String for every instance name with a RegEx
    """
    pattern = r'[A-Z0-9]{23,24}'
    try:
        return [match.group() for match in re.finditer(pattern, text)]
    except Exception:
        raise Exception("Error in finding instance names within regex text. Make sure the injected string has been extracted correctly, analysis of code is required.")