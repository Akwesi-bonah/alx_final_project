#!/usr/bin/env python3
"""Test cases for the Reservation class."""
import unittest
from models.reservation import Reservation

class TestReservation(unittest.TestCase):
    """Test cases for the Reservation class."""
    def setUp(self):
        """ Create an instance of Reservation for testing """
        self.reservation = Reservation()

    def test_room_default_value(self):
        """ Check if the default value of room is an empty string """
        self.assertEqual(self.reservation.room, "")

    def test_description_default_value(self):
        """ Check if the default value of description is an empty string """
        self.assertEqual(self.reservation.description, "")

    def test_number_of_guests_default_value(self):
        """ Check if the default value of number_of_guests is 0 """
        self.assertEqual(self.reservation.number_of_guests, 0)

    def test_init_method(self):
        """ Check if the __init__ method initializes the attributes correctly """
        reservation = Reservation(room="101", description="Single room", number_of_guests=1)
        self.assertEqual(reservation.room, "101")
        self.assertEqual(reservation.description, "Single room")
        self.assertEqual(reservation.number_of_guests, 1)

if __name__ == '__main__':
    unittest.main()