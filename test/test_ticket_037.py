import unittest
from src.ticket_037 import *


class TestTicket037(unittest.TestCase):

    def setUp(self):
        with open("../assets/Example MDR Events/MDR_Event_1.json") as self.json_file_1, \
                open("../assets/Example MDR Events/MDR_Event_2.json") as self.json_file_2, \
                open("../assets/Example MDR Events/MDR_Event_3.json") as self.json_file_3, \
                open("../assets/Example MDR Events/MDR_Event_4.json") as self.json_file_4:
            self.data_1 = json.load(self.json_file_1)
            self.data_2 = json.load(self.json_file_2)
            self.data_3 = json.load(self.json_file_3)
            self.data_4 = json.load(self.json_file_4)

    def tearDown(self):
        self.json_file_1.close()
        self.json_file_2.close()
        self.json_file_3.close()
        self.json_file_4.close()

    def test_mdr_get_sys_name(self):
        self.assertEqual("ubuntu-share01", mdr_get_sys_name(self.data_1), "MDR_Event_1")
        self.assertEqual("ubuntu-share01", mdr_get_sys_name(self.data_2), "MDR_Event_2")
        self.assertEqual("ubuntu-share01", mdr_get_sys_name(self.data_3), "MDR_Event_3")
        self.assertEqual("ubuntu-share01", mdr_get_sys_name(self.data_4), "MDR_Event_4")

        self.assertNotEquals("ubuntu-share0", mdr_get_sys_name(self.data_1), "MDR_Event_1_2")


if __name__ == '__main__':
    unittest.main()
