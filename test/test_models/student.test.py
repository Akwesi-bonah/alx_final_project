#!/usr/bin/env python3
""" test student module for student model """
import unittest
from datetime import date
from models.student import Student

class TestStudent(unittest.TestCase):
    """ Test cases for the Student class."""
    def setUp(self):
        self.student = Student(
            first_name="John",
            last_name="Doe",
            date_of_birth=date(2000, 1, 1),
            gender="Male",
            student_number="123456",
            program="Computer Science",
            level="Undergraduate",
            email="john.doe@example.com",
            address="123 Main St",
            phone="1234567890",
            guardian_name="Jane Doe",
            guardian_phone="0987654321",
            password="password123",
            disability="None"
        )

    def test_name(self):
        """Test for the first name and last name attributes."""
        self.assertEqual(self.student.first_name, "John")
        self.assertEqual(self.student.last_name, "Doe")

    def test_date_of_birth(self):
        """Test for the date of birth attribute."""
        self.assertEqual(self.student.date_of_birth, date(2000, 1, 1))

    def test_gender(self):
        """Test for the gender attribute."""
        self.assertEqual(self.student.gender, "Male")

    def test_student_number(self):
        """Test for the student number attribute."""
        self.assertEqual(self.student.student_number, "123456")

    def test_program(self):
        """Test for the program attribute."""
        self.assertEqual(self.student.program, "Computer Science")

    def test_level(self):
        """Test for the level attribute."""
        self.assertEqual(self.student.level, "Undergraduate")

    def test_email(self):
        """Test for the email attribute."""
        self.assertEqual(self.student.email, "john.doe@example.com")

    def test_address(self):
        """Test for the address attribute."""
        self.assertEqual(self.student.address, "123 Main St")

    def test_phone(self):
        """Test for the phone attribute."""
        self.assertEqual(self.student.phone, "1234567890")

    def test_guardian_name(self):
        """Test for the guardian name attribute."""
        self.assertEqual(self.student.guardian_name, "Jane Doe")

    def test_guardian_phone(self):
        """"Test for guardian phone attribute."""
        self.assertEqual(self.student.guardian_phone, "0987654321")

    def test_password_encryption(self):
        """Test for the password attribute."""
        self.assertNotEqual(self.student.password, "password123")
        self.assertTrue(self.student.password.startswith("$2"))

    def test_disability(self):
        """Test for the disability attribute."""
        self.assertEqual(self.student.disability, "None")

    def test_str_representation(self):
        """Test for the __str__ method."""
        self.assertEqual(str(self.student), "John Doe")

    
if __name__ == "__main__":
    unittest.main()