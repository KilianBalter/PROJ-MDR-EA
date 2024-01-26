import unittest

from src.my_credentials import get_credentials
from src.ea_login_functions import get_jwt_token
from src.ea_rules_access_functions import get_hardening_variation_key_by_id


class TestHardeningVariationKey(unittest.TestCase):

    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_hardening_variation_key_by_id(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        key = get_hardening_variation_key_by_id(token, '1')
        self.assertEqual(key, "W11_Essential___1_0", "Variation Key Extraction not working!")


if __name__ == '__main__':
    unittest.main()
