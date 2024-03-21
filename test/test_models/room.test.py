import unittest
from models.room import Room

class TestRoom(unittest.TestCase):
    def setUp(self):
        # Create a sample room object for testing
        self.room = Room(
            block_id="block1",
            room_type_id="type1",
            room_name="Room 101",
            gender="Male",
            floor="1st",
            no_of_beds=4,
            booked_beds=2,
            reserved_beds=1,
            status="Available"
        )

    def test_room_attributes(self):
        # Check if the room object has the correct attributes
        self.assertEqual(self.room.block_id, "block1")
        self.assertEqual(self.room.room_type_id, "type1")
        self.assertEqual(self.room.room_name, "Room 101")
        self.assertEqual(self.room.gender, "Male")
        self.assertEqual(self.room.floor, "1st")
        self.assertEqual(self.room.no_of_beds, 4)
        self.assertEqual(self.room.booked_beds, 2)
        self.assertEqual(self.room.reserved_beds, 1)
        self.assertEqual(self.room.status, "Available")

    def test_room_initialization(self):
        # Check if the room object is initialized correctly
        self.assertIsInstance(self.room, Room)
        self.assertEqual(self.room.block, "")
        self.assertEqual(self.room.room_type, "")
        self.assertEqual(self.room.room_name, "")
        self.assertEqual(self.room.gender, "")
        self.assertEqual(self.room.floor, "")
        self.assertEqual(self.room.no_of_beds, 0)

if __name__ == '__main__':
    unittest.main()