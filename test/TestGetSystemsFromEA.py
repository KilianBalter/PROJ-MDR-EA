import unittest

from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.ea_system_identification_functions import get_all_systems


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
