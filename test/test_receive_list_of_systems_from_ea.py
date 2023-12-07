import unittest

import json
import src.obtain_a_JWT_token as tokenReceive
import src.receive_list_of_systems_from_ea as systemList
class TestListOfSystemsFromEA(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_login(self):
        token = tokenReceive.get_jwt_token("", "")
        self.assertIsNot(None, token, "Token not received. Please check VPN, credentials")

    def test_system_list(self):
        token = tokenReceive.get_jwt_token("", "")
        response = systemList.get_list_of_systems_from_ea(token)
        name = response.json()[0]['name']
        self.assertEqual(name, "DESKTOP-GSLP39T", "System list retrieving not working!")




if __name__ == '__main__':
    unittest.main()
