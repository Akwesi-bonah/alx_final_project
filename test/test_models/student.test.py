import unittest
from datetime import date
from models.student import Student

class TestStudent(unittest.TestCase):
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

    def test_full_name(self):
        self.assertEqual(self.student.first_name, "John")
        self.assertEqual(self.student.last_name, "Doe")
        self.assertEqual(self.student.full_name, "John Doe")

    def test_date_of_birth(self):
        self.assertEqual(self.student.date_of_birth, date(2000, 1, 1))

    def test_gender(self):
        self.assertEqual(self.student.gender, "Male")

    def test_student_number(self):
        self.assertEqual(self.student.student_number, "123456")

    def test_program(self):
        self.assertEqual(self.student.program, "Computer Science")

    def test_level(self):
        self.assertEqual(self.student.level, "Undergraduate")

    def test_email(self):
        self.assertEqual(self.student.email, "john.doe@example.com")

    def test_address(self):
        self.assertEqual(self.student.address, "123 Main St")

    def test_phone(self):
        self.assertEqual(self.student.phone, "1234567890")

    def test_guardian_name(self):
        self.assertEqual(self.student.guardian_name, "Jane Doe")

    def test_guardian_phone(self):
        self.assertEqual(self.student.guardian_phone, "0987654321")

    def test_password_encryption(self):
        self.assertNotEqual(self.student.password, "password123")
        self.assertTrue(self.student.password.startswith("$2"))

    def test_disability(self):
        self.assertEqual(self.student.disability, "None")

    def test_str_representation(self):
        self.assertEqual(str(self.student), "John Doe")

    def test_get_id(self):
        self.assertEqual(self.student.get_id, str(self.student.id))

if __name__ == "__main__":
    unittest.main()