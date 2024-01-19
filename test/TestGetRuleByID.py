import json
import unittest

from src.my_credentials import get_credentials
from src.handle_data import get_jwt_token
from src.handle_data import get_rule_by_instance_name


class TestGetRuleByID(unittest.TestCase):
    def setUp(self):
        self.credentials = get_credentials()
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_rule_by_id(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        rule = get_rule_by_instance_name(token, '8081C25334A33DC8F2389B7F')
        self.assertEqual(55, json.loads(rule)['id'], "Rule not extracted correctly")


if __name__ == '__main__':
    unittest.main()
