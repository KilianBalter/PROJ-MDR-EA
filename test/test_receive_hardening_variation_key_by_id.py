import unittest

import json
import src.obtain_a_JWT_token as tokenReceive
import src.receive_hardening_variation_key_by_id as variationKey
class TestHardeningVariationKey(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_login(self):
        token = tokenReceive.get_jwt_token("", "")
        self.assertIsNot(None, token, "Token not received. Please check VPN, credentials")

    def test_system_list(self):
        token = tokenReceive.get_jwt_token("", "")
        key = variationKey.get_hardening_variation_key_by_id(token,1)
        self.assertEqual(key, "W11_Essential___1_0", "Variation Key Extraction not working!")


if __name__ == '__main__':
    unittest.main()