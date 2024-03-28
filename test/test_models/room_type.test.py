#!/usr/bin/env python3
""" test room_type module for room_type model 
"""
import unittest
from models.room_type import RoomType

class TestRoomType(unittest.TestCase):
    """ Test case for the RoomType class."""
    def setUp(self):
        """ Create an instance of RoomType for testing """
        self.room_type = RoomType()

    def test_default_values(self):
        """ Check if the default values are set correctly """
        self.assertEqual(self.room_type.name, "")
        self.assertEqual(self.room_type.description, "")
        self.assertEqual(self.room_type.price, 0.0)
        self.assertEqual(self.room_type.status, "")

    def test_initialization(self):
        """ Check if the initialization sets the attributes correctly """
        room_type = RoomType(name="Single Room", description="A cozy single room", price=100.0, status="Available")
        self.assertEqual(room_type.name, "Single Room")
        self.assertEqual(room_type.description, "A cozy single room")
        self.assertEqual(room_type.price, 100.0)
        self.assertEqual(room_type.status, "Available")

    def test_str_representation(self):
        """ Check if the __str__ method returns the expected string representation """
        room_type = RoomType(name="Double Room", description="A spacious double room", price=150.0, status="Booked")
        expected_str = "RoomType(name='Double Room', description='A spacious double room', price=150.0, status='Booked')"
        self.assertEqual(str(room_type), expected_str)

if __name__ == '__main__':
    unittest.main()