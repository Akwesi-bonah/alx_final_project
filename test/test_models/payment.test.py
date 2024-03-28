#!/usr/bin/env python3
""" test payment module for payment model """


import unittest
from models.payment import Payment

class TestPayment(unittest.TestCase):

    """Test case for the Payment class."""
    def setUp(self):
        """ Create an instance of Payment for testing """
        self.payment = Payment()

    def test_default_values(self):
        """ Check if the default values are set correctly """
        self.assertEqual(self.payment.student_number, "")
        self.assertEqual(self.payment.room_name, "")
        self.assertEqual(self.payment.amount, 0)

    def test_init_method(self):
        """ Check if the __init__ method initializes the attributes correctly """
        payment = Payment(student_number="12345", room_name="Room 101", amount=100.00)
        self.assertEqual(payment.student_number, "12345")
        self.assertEqual(payment.room_name, "Room 101")
        self.assertEqual(payment.amount, 100.00)

    def test_str_method(self):
        """" Check if the __str__ method returns the expected string representation """
        payment = Payment(student_number="12345", room_name="Room 101", amount=100.00)
        expected_str = "Payment(student_number='12345', room_name='Room 101', amount=100.00)"
        self.assertEqual(str(payment), expected_str)

    
if __name__ == '__main__':
    unittest.main()