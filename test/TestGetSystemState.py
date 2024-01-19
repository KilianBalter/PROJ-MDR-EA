import unittest
from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.get_the_state_of_the_system import get_the_state


class TestGetSystemState(unittest.TestCase):

    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_hardening_variation_key_by_id(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        status = get_the_state(token, '1')
        self.assertEqual(status, True, "State extraction Not working")


if __name__ == '__main__':
    unittest.main()
