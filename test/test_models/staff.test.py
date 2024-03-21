import unittest
from models.staff import Staff

class TestStaff(unittest.TestCase):
    def setUp(self):
        # Create a sample staff object for testing
        self.staff = Staff(
            campus="Campus A",
            name="John Doe",
            email="johndoe@example.com",
            phone="1234567890",
            password="password123",
            role="Admin",
            status="Active"
        )

    def test_attributes(self):
        # Test if the attributes are set correctly
        self.assertEqual(self.staff.campus, "Campus A")
        self.assertEqual(self.staff.name, "John Doe")
        self.assertEqual(self.staff.email, "johndoe@example.com")
        self.assertEqual(self.staff.phone, "1234567890")
        self.assertNotEqual(self.staff.password, "password123")  # Password should be hashed
        self.assertEqual(self.staff.role, "Admin")
        self.assertEqual(self.staff.status, "Active")

    def test_str(self):
        # Test the __str__ method
        self.assertEqual(str(self.staff), "John Doe")

    def test_get_id(self):
        # Test the get_id method
        self.assertIsNone(self.staff.get_id())  # Assuming id is not set in the constructor

    def test_password_encryption(self):
        # Test if the password is encrypted using md5
        password_hash = self.staff.password
        self.assertTrue(password_hash.startswith("$md5$"))

if __name__ == "__main__":
    unittest.main()