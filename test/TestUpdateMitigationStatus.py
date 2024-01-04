import unittest
import json

from src.my_credentials import get_credentials
from src.obtain_a_JWT_token import get_jwt_token
from src.update_mitigation_status import update_mitigation_status


class TestAddMitigationStatus(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")
        with open("../assets/Example MDR Events/Test_Event_1.json") as self.json_file_1, \
                open("../assets/Example MDR Events/Test_Event_2.json") as self.json_file_2:
            self.data_1 = json.load(self.json_file_1)
            self.data_2 = json.load(self.json_file_2)

    def tearDown(self):
        self.json_file_2.close()
        self.json_file_1.close()
        print("\nEnding Unittest\n")

    def test_add_mitigation_status(self):
        credentials = get_credentials()
        token = get_jwt_token(credentials['username'], credentials['password'])

        hardening_info = {
            "satisfied_mitigations": {
                "M1040": {
                    "description": "On Windows 10, enable Attack Surface Reduction (ASR) rules to prevent Visual Basic and JavaScript scripts from executing potentially malicious downloaded content.",
                    "rules": {
                        1608: {
                            "title": "(L1) Ensure 'Configure Attack Surface Reduction rules: Block JavaScript or VBScript from launching downloaded executable content'"
                        }
                    }
                }
            },
            "unsatisfied_mitigations": {},
            "vulnerability_status": "NOT_VULNERABLE",
        }

        satisfied_mitigations = {
            'M1040': {
                "description": "On Windows 10, enable Attack Surface Reduction (ASR) rules to prevent Visual Basic and JavaScript scripts from executing potentially malicious downloaded content.",
                'rules': [1608]
            }
        }
        unsatisfied_mitigations = {}

        update_mitigation_status(self.data_1, token, satisfied_mitigations, unsatisfied_mitigations)

        rules = self.data_1['hardening_info']['satisfied_mitigations']['M1040']['rules']
        self.assertTrue(all(rules[rule]['title'] for rule in rules), "Missing titles")
        self.assertEqual(hardening_info, self.data_1['hardening_info'], "Hardening info doesn't match")


if __name__ == '__main__':
    unittest.main()
