# unit test case
import unittest

from src.controllers.trip_controller import gets2id, getSpeed

import logging


class TestStringMethods(unittest.TestCase):
    # unit test function to test S2 ID
    def testSid(self):
        actual = gets2id(41.901206994, -87.676355989)
        logging.warning(actual)
        expected = 9804286676955037696
        # error message in case test case got failed
        message = "Failed!"
        # assertEqual() to check equality of first & second value
        self.assertEqual(actual, expected, message)

    # unit test function to test Speed
    def testSpeed(self):
        actual = getSpeed(10, 600)
        logging.warning(actual)
        expected = 96.5604
        message = "Failed!"
        self.assertEqual(actual, expected, message)


if __name__ == '__main__':
    unittest.main()
