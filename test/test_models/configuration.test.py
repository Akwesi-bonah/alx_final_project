#!/usr/bin/env python3
""" test configuration module   """
import unittest
from datetime import datetime
from models.configuration import Configuration
from models.staff import Staff


class TestConfiguration(unittest.TestCase):
    """
    Test case for the Configuration class.
    """

    def setUp(self):
        """ initialize configration clask """
        self.staff = Staff(id=1, name="John Doe")
        self.configuration = Configuration(created_by=self.staff, expiry_date=datetime(2022, 12, 31))

    def test_created_by(self):
        """ test created by"""
        self.assertEqual(self.configuration.created_by, self.staff)

    def test_expiry_date(self):
        """Test expiry data attribute"""
        self.assertEqual(self.configuration.expiry_date, datetime(2022, 12, 31))

    def test_created_by_default_value(self):
        """Test defualt value"""
        configuration = Configuration()
        self.assertEqual(configuration.created_by, "")

    def test_expiry_date_default_value(self):
        configuration = Configuration()
        self.assertEqual(configuration.expiry_date, "")

if __name__ == '__main__':
    unittest.main()