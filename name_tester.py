import unittest
from window import main

class TestTimeClock(unittest.TestCase):

    def setUp(self):
        # Set up any necessary objects or configurations before each test
        pass

    def tearDown(self):
        # Clean up after each test
        pass

    def test_valid_names(self):
        # Test when valid first and last names are provided
        # Replace 'John' and 'Doe' with your actual test data
        result = main.validate_names('John', 'Doe')
        self.assertTrue(result)  # Assert that the result is True for valid names

    def test_invalid_first_name(self):
        # Test when an invalid first name is provided
        # Replace '123' with your actual test data
        result = main.validate_names('123', 'Doe')
        self.assertFalse(result)  # Assert that the result is False for an invalid first name

    def test_invalid_last_name(self):
        # Test when an invalid last name is provided
        # Replace 'John' and '456' with your actual test data
        result = main.validate_names('John', '456')
        self.assertFalse(result)  # Assert that the result is False for an invalid last name

if __name__ == '__main__':
    unittest.main()
