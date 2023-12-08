import unittest

from src.extract_ea_system_id import get_ea_system_id_from_list_of_systems


class TestExtractEASystemID(unittest.TestCase):

    def setUp(self):
        print("\nStarting Unittest.\n")

    def tearDown(self):
        print("\nEnding Unittest\n")

    def test_get_ea_system_id_from_list_of_systems(self):
        example_mdr_name = 'desktop-gslp39T'
        example_list = [{'name': 'DESKTOP-GSLP39T', 'fqdn': 'DESKTOP-GSLP39T.', 'description': None,
                         'installationDate': '2023-11-17T00:00:00', 'decommissioningDate': None,
                         'trashId': '00000000-0000-0000-0000-000000000000', 'domainId': 2,
                         'domainName': 'ThEagleEnforce.local', 'domainNetbiosName': 'ThEagleEnforce',
                         'responsibleContactId': 1, 'responsibleContactName': 'EnforceLabsTeam',
                         'responsibleContactShortName': 'EnforceLabsTeam', 'operatingSystemId': 1,
                         'operatingSystemName': 'Windows 11 (21H2)', 'operatingSystemShortName': 'w11.21h2',
                         'stageId': 1, 'stageName': 'Production', 'stageShortName': 'Prd', 'serverRoleId': 2,
                         'serverRoleName': 'Windows 11 Client', 'serverRoleShortName': 'W11Client',
                         'joinTypeId': 1, 'joinTypeName': 'Active Directory Domain Services',
                         'joinTypeShortName': 'ADDS',
                         'osLanguageId': 2, 'osLanguageDecimalId': 2057, 'osLanguageTag': 'en-GB',
                         'osLanguageName': 'English (United Kingdom)', 'isDeleted': False, 'isActive': True,
                         'isDecommissioned': False, 'additionalProperties': '{}',
                         'createdOn': '2023-11-17T14:34:57.3734697', 'lastChanged': '2023-11-17T14:45:26.2034979',
                         'id': 1}]
        self.assertEqual(get_ea_system_id_from_list_of_systems(example_list, example_mdr_name), "1", "Incorrect ID")


if __name__ == '__main__':
    unittest.main()
