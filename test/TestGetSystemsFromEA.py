import unittest

from src.my_credentials import get_credentials
from src.handle_data import get_jwt_token
from src.handle_data import get_all_systems


class TestGetSystemsFromEA(unittest.TestCase):
    def setUp(self):
        self.credentials = get_credentials()
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_login(self):
        token = get_jwt_token(self.credentials['username'], self.credentials['password'])
        self.assertIsNot(None, token, "Token not received. Please check VPN, credentials")

    def test_system_list(self):
        token = get_jwt_token(self.credentials['username'], self.credentials['password'])
        systems = get_all_systems(token)
        name = systems[0]['name']
        self.assertEqual(name, "DESKTOP-GSLP39T", "System list retrieving not working!")


if __name__ == '__main__':
    unittest.main()
