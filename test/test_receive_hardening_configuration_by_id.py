import unittest
import src.ea_login_functions as tokenReceive
from src.my_credentials import get_credentials
from src.receive_hardening_configuration_by_id import get_hardening_configuration_template_by_id


class TestHardeningConfiguration(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_receive_hardening_configuration(self):
        credentials = get_credentials()
        token = tokenReceive.get_jwt_token(credentials['username'], credentials['password'])
        information = get_hardening_configuration_template_by_id(token, "2")
        self.assertIsNotNone(information,"Information retrieve failed!")


if __name__ == '__main__':
    unittest.main()
