from src.my_credentials import get_credentials
from src.handle_data import get_jwt_token
from src.handle_data import get_hardening_id

import unittest


class TestGetHardeningID(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_hardening_id(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        self.assertEqual(get_hardening_id(token, "W11_Essential___1_0"), 1, "Incorrect ID")


if __name__ == '__main__':
    unittest.main()
