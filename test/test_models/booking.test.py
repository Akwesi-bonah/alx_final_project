import unittest
from datetime import datetime
import pep8 as pycodestyle
from models.booking import Booking


class TestBookingDocs(unittest.TestCase):
    """Tests to check the documentation and style of Booking class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.base_funcs = inspect.getmembers(Booking, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in ['models/booking.py',
                     'tests/test_models/booking_test.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_class_docstring(self):
        """Test for the Booking class docstring"""
        self.assertIsNot(Booking.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(Booking.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in Booking methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0])
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0])
                )


class TestBooking(unittest.TestCase):
    def setUp(self):
        """ Create a sample booking object for testing """
        self.booking = Booking(room_id="123", student_id="456", paid="100", status="pending")

    def test_initialization(self):
        """ Check if the booking object is initialized correctly """
        self.assertEqual(self.booking.room_id, "123")
        self.assertEqual(self.booking.student_id, "456")
        self.assertEqual(self.booking.paid, "100")
        self.assertEqual(self.booking.status, "pending")

    def test_default_values(self):
        """ Check if the default values are set correctly """
        booking = Booking()
        self.assertEqual(booking.room_name, "")
        self.assertEqual(booking.room_type, "")
        self.assertEqual(booking.paid, "")
        self.assertEqual(booking.status, "")

    def test_update_values(self):
        """ Check if the values can be updated correctly """
        self.booking.room_id = "789"
        self.booking.student_id = "012"
        self.booking.paid = "200"
        self.booking.status = "pending"

        self.assertEqual(self.booking.room_id, "789")
        self.assertEqual(self.booking.student_id, "012")
        self.assertEqual(self.booking.paid, "200")
        self.assertEqual(self.booking.status, "pending")

    def test_string_representation(self):
        """ Check if the string representation of the booking object is correct """
        expected_string = "Booking(room_id='123', student_id='456', paid='100', status='pending')"
        self.assertEqual(str(self.booking), expected_string)

if __name__ == '__main__':
    unittest.main()