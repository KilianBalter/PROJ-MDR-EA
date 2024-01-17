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

        # -------------------------------------------
        # | Partial | Rules present | Result        |
        # |  False  |      ALL      |  SATISFIED    |
        # |  False  |      SOME     |  PARTIAL      |
        # |  False  |      NONE     |  UNSATISFIED  |
        # |  True   |      ALL      |  PARTIAL      |
        # |  True   |      SOME     |  PARTIAL      |
        # |  True   |      NONE     |  UNSATISFIED  |
        # -------------------------------------------
        mitigations = {
            # Partial False, ALL rules present
            "M1040": {
                "partial": False,
                "description": "On Windows 10, enable Attack Surface Reduction (ASR) rules to prevent Visual" +
                " Basic and JavaScript scripts from executing potentially malicious downloaded content.",
                "rules": [
                    1608
                ]
            },
            # Partial False, SOME rules present
            "M1041": {
                "partial": False,
                "description": "Test",
                "rules": [
                    1608,
                    4822
                ]
            },
            # Partial False, NO rules present
            "M1042": {
                "partial": False,
                "description": "Test",
                "rules": [
                    11,
                    12
                ]
            },
            # Partial True, ALL rules present
            "M1043": {
                "partial": True,
                "description": "Test",
                "rules": [
                    82,
                    83
                ]
            },
            # Partial True, SOME rules present
            "M1044": {
                "partial": True,
                "description": "Test",
                "rules": [
                    44,
                    82
                ]
            },
            # Partial True, NO rules present
            "M1045": {
                "partial": True,
                "description": "Test",
                "rules": [
                    10,
                    20
                ]
            }
        }

        satisfied_mitigations, partial_mitigations, unsatisfied_mitigations = check_mapping(mitigations, rule_ids)
        self.assertEqual(['M1040'], list(satisfied_mitigations.keys()),
                         "Mitigations not correctly detected")
        self.assertEqual(['M1041', 'M1043', 'M1044'], list(partial_mitigations.keys()),
                         "Mitigations not correctly detected")
        self.assertEqual(['M1042', 'M1045'], list(unsatisfied_mitigations.keys()),
                         "Mitigations not correctly detected")


if __name__ == '__main__':
    unittest.main()
