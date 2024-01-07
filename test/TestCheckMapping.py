import unittest

from src.check_mapping import check_mapping


class TestCheckMapping(unittest.TestCase):
    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_check_mapping(self):
        rule_ids = [
            55, 66, 70, 71, 73, 74, 75, 76, 77, 82, 83, 84, 85, 86, 87, 88, 89, 99, 100, 237, 238, 245, 246, 247, 248,
            250, 310, 330, 495, 612, 778, 811, 816, 857, 862, 895, 1603, 1604, 1605, 1606, 1607, 1608, 1609, 1610,
            1611, 1612, 1613, 1615, 1984, 1995, 1996, 2013, 2014, 2015, 2016, 2024, 2025, 2026, 2027, 2116, 2117,
            4014, 4027, 4044, 4226, 4228, 4229, 4230, 4231, 4232, 4233, 4234, 4235, 4236, 4237, 4238, 4239, 4240,
            4241, 4242, 4243, 4244, 4245, 4246, 4247, 4248, 4249, 4250, 4251, 4252, 4253, 4254, 4255, 4256, 4257,
            4258, 4259, 4260, 4261, 4262, 4263, 4264, 4265, 4266, 4267, 4268, 4269, 4270, 4271, 4272, 4273, 4274,
            4275, 4276, 4277, 4278, 4279, 4280, 4281,
        ]

        mitigations = {
                "M1040": {
                    "description": "On Windows 10, enable Attack Surface Reduction (ASR) rules to prevent Visual" +
                    " Basic and JavaScript scripts from executing potentially malicious downloaded content.",
                    "rules": [
                        1608
                    ]
                }
        }

        satisfied_mitigations, unsatisfied_mitigations = check_mapping(mitigations, rule_ids)
        self.assertEqual(['M1040'], list(satisfied_mitigations.keys()), "Mitigations not correctly detected")
        self.assertEqual([], list(unsatisfied_mitigations.keys()), "Mitigations not correctly detected")

        rule_ids = [5, 10, 20]

        satisfied_mitigations, unsatisfied_mitigations = check_mapping(mitigations, rule_ids)
        self.assertEqual([], list(satisfied_mitigations.keys()), "Mitigations not correctly detected")
        self.assertEqual(['M1040'], list(unsatisfied_mitigations.keys()), "Mitigations not correctly detected")


if __name__ == '__main__':
    unittest.main()
