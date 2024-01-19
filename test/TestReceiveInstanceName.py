import unittest

from src.my_credentials import get_credentials
from src.handle_data import get_jwt_token
from src.handle_data import get_hardening_configuration_template_by_id
from src.handle_data import receive_instance_name


class TestReceiveInstanceName(unittest.TestCase):

    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_receive_instance_name_with_code_template(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])
        code_template = get_hardening_configuration_template_by_id(token, "2")
        instance_names = receive_instance_name(code_template)
        self.assertIsNot(instance_names, str, "there was no Code Template provided")
        self.assertIsNot(instance_names, [], "there were no xRegistry instance_names in the code_template")
        self.assertEqual(instance_names[0], '8081C25334A33DC8F2389B7F', "did not find the correct template")
        self.assertEqual(instance_names[len(instance_names) - 1], 'C2391B82940E7FD6758AA0C', "did not find the "
                                                                                             "correct template")

    def test_receive_instance_name_without_code_template(self):
        instance_names = receive_instance_name(None)
        self.assertEqual(instance_names, '', "the behaviour of the receive_instance_name function in case of no "
                                             "code_template is not correct")


if __name__ == '__main__':
    unittest.main()
