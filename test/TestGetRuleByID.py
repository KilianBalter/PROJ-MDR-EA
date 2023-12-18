import json
import unittest

from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.get_rule_by_id import get_rule_by_instance_name


class TestGetRuleByID(unittest.TestCase):
    def setUp(self):
        self.credentials = get_credentials()
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_rule_by_id(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        print(json.dumps(get_rule_by_instance_name(token, '8081C25334A33DC8F2389B7F')))


if __name__ == '__main__':
    unittest.main()
