import unittest
from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.receive_the_instance_name import receive_instance_name


class TestReceiveInstanceName(unittest.TestCase):

    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_hardening_variation_key_by_id(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        dsc_id = receive_instance_name(token, '1')
        self.assertEqual(dsc_id, 1, "dsc_Id extraction not working")


if __name__ == '__main__':
    unittest.main()
