import unittest

from src.my_credentials import get_credentials
from src.handle_data import get_jwt_token
from src.handle_data import get_rule_ids


class TestGetRuleIDs(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_rule_ids(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        rule_ids = get_rule_ids(token, '1')
        self.assertEqual(55, rule_ids[0], "Id at position 0 does not match expected Id")
        self.assertEqual(66, rule_ids[1], "Id at position 1 does not match expected Id")
        self.assertEqual(70, rule_ids[2], "Id at position 2 does not match expected Id")
        self.assertEqual(4679, rule_ids[-3], "Id at position 533 does not match expected Id")
        self.assertEqual(4680, rule_ids[-2], "Id at position 534 does not match expected Id")
        self.assertEqual(4681, rule_ids[-1], "Id at position 535 does not match expected Id")
        self.assertEqual(467, len(rule_ids), "Length of rule_ids array does not match expected value")


if __name__ == '__main__':
    unittest.main()
