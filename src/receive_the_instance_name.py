import json

from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.receive_hardening_configuration_by_id import get_hardening_configuration_template_by_id


def receive_instance_name(auth_token: str, code_template: json) -> str:
    if not code_template:
        return ''

    str_code_template = str(code_template)


if __name__ == "__main__":
    credentials = get_credentials()
    token = get_jwt_token(credentials["username"], credentials["password"])
    code_template = get_hardening_configuration_template_by_id(token, "2")
    receive_instance_name(token, code_template)
