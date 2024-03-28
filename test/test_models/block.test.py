#!/usr/bin/python3
"""Unittest for block.py"""
import unittest
from models.block import Block
import pep8 as pycodestyle
import inspect
block_doc = Block.__doc__


class TestBlockDocs(unittest.TestCase):
    """Tests to check the documentation and style of block class"""

    @classmethod
    def setUpClass(cls):
        """Set up for docstring tests"""
        cls.base_funcs = inspect.getmembers(Block, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base.py conforms to PEP8."""
        for path in ['models/block.py',
                     'tests/test_models/block_test.py']:
            with self.subTest(path=path):
                errors = pycodestyle.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(Block.__doc__, None,
                         "BaseModel class needs a docstring")
        self.assertTrue(len(Block.__doc__) >= 1,
                        "BaseModel class needs a docstring")

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""

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


class TestBlockCreation(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.block_data = {
            'campus': 'Campus A',
            'name': 'Block A',
            'description': 'This is Block A'
        }

    def test_block_creation_with_data(self):
        """Test block creation with data"""
        block = Block(**self.block_data)
        self.assertEqual(block.campus, self.block_data['campus'])
        self.assertEqual(block.name, self.block_data['name'])
        self.assertEqual(block.description, self.block_data['description'])

    def test_block_creation_with_default_values(self):
        """Test block creation with default values"""
        block = Block()
        self.assertEqual(block.campus, "")
        self.assertEqual(block.name, "")
        self.assertEqual(block.description, "")

    def test_block_creation_with_empty_data(self):
        """Test block creation with empty data"""
        block = Block(campus="", name="", description="")
        self.assertEqual(block.campus, "")
        self.assertEqual(block.name, "")
        self.assertEqual(block.description, "")

    def test_block_creation_with_missing_data(self):
        """Test block creation with missing data"""
        block = Block(campus="Campus A")
        self.assertEqual(block.campus, "Campus A")
        self.assertEqual(block.name, "")
        self.assertEqual(block.description, "")

    def test_block_creation_with_extra_data(self):
        """Test block creation with extra data"""
        block = Block(**self.block_data, extra="Extra Data")
        self.assertEqual(block.campus, self.block_data['campus'])
        self.assertEqual(block.name, self.block_data['name'])
        self.assertEqual(block.description, self.block_data['description'])

    def test_block_str_representation(self):
        """Test block string representation"""
        block = Block(**self.block_data)
        expected_str = f"Block: {block.name} - {block.description}"
        self.assertEqual(str(block), expected_str)

    def test_block_str_representation_with_empty_data(self):
        """Test block string representation with empty data"""
        block = Block(campus="", name="", description="")
        expected_str = "Block: - "
        self.assertEqual(str(block), expected_str)

    def test_block_str_representation_with_missing_data(self):
        """Test block string representation with missing data"""
        block = Block(campus="Campus A")
        expected_str = "Block: - "
        self.assertEqual(str(block), expected_str)

    def test_block_str_representation_with_extra_data(self):
        """Test block string representation with extra data"""
        block = Block(**self.block_data, extra="Extra Data")
        expected_str = f"Block: {block.name} - {block.description}"
        self.assertEqual(str(block), expected_str)

    def test_block_object_equality(self):
        """Test block object equality"""
        block1 = Block(**self.block_data)
        block2 = Block(**self.block_data)
        self.assertEqual(block1, block2)

    def test_block_object_inequality(self):
        """Test block object inequality"""
        block1 = Block(campus="Campus A", name="Block A", description="This is Block A")
        block2 = Block(campus="Campus B", name="Block B", description="This is Block B")
        self.assertNotEqual(block1, block2)


if __name__ == '__main__':
    unittest.main()