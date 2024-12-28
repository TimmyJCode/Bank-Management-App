# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain the test interface for the reusable utility functions found in
# the utilities.py file

import unittest
from user import *
from utilities import *
from errors import *

# Test isValidRole function
class TestIsValidRole(unittest.TestCase):
    # Test with valid roles
    def test_valid_role(self):
        self.assertTrue(isValidRole("customer"))
        self.assertTrue(isValidRole("admin"))
    # Test with invalid roles
    def test_invalid_role(self):
        self.assertFalse(isValidRole("moderator"))
        self.assertFalse(isValidRole("user"))
        self.assertFalse(isValidRole(1234))
        self.assertFalse(isValidRole(""))

# Test PasswordService class
class TestPasswordService(unittest.TestCase):
    # Test hashPassword function
    def test_hash_password(self):
        # Test with valid password
        hashedPassword = PasswordService.hashPassword("Password123!")
        self.assertTrue(PasswordService.checkPassword("Password123!", hashedPassword))
    # Test validatePassword function
    def test_validate_password(self):
        # Test with valid password
        self.assertIsNone(PasswordService.validatePassword("Password123!"))
        # Test with invalid password
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("pass")
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("password123!")
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("Password")
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("password")
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("Password123")
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("Password!")
        with self.assertRaises(InvalidPasswordError):
            PasswordService.validatePassword("Password 123!")