# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain the test interface for the user class and its derived customer
# and admin classes

import unittest
import pytest
from passlib.hash import bcrypt
from datetime import datetime, date
from unittest.mock import patch
from user import *
from utilities import *

# Test the user class
class TestUser(unittest.TestCase):
    # Create a valid user for testing
    @pytest.fixture()
    def validUser(self):
        return User("Timmons001", "J@cksPassword1234", "jacktimmonsemail@gmail.com")

    # Test the user class constructor
    # Test with valid data
    def test_user_constructor_valid(self):
        # Create a valid user
        newUser = User("Timmons001", "J@cksPassword1234", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
        # Check that the user's ID is correct
        self.assertEqual(newUser.userID, "Timmons001")
        # Check that the users hashed password is correct
        self.assertTrue(newUser.checkPassword("J@cksPassword1234"))
        # Check that the user's email is correct
        self.assertEqual(newUser.email, "jacktimmonsemail@gmail.com")
        # Check that the user's role is correct
        self.assertEqual(newUser.role, "customer")
        # Check that the user's first name is correct
        self.assertEqual(newUser.firstName, "Jack")
        # Check that the user's last name is correct
        self.assertEqual(newUser.lastName, "Timmons")
        # Check that the user's DOB is correct
        self.assertEqual(newUser.DOB.strftime("%m/%d/%Y"), "03/27/1996")
        # Check that the user's password is hashed correctly
    # Test with invalid ID (not a string)
    def test_user_constructor_invalid_id_non_string(self):
        with self.assertRaises(TypeError, msg = "User ID must be a string"):
            newUser = User(123, "J@cksPassword1234", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
    # Test with invalid ID (empty string)
    def test_user_constructor_invalid_id_empty(self):
        with self.assertRaises(ValueError, msg = "User ID cannot be empty"):
            newUser = User("", "J@cksPassword1234", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
    # Test with invalid password (too short)
    def test_user_constructor_invalid_password_too_short(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password must be at least 8 characters long"):
            newUser = User("Timmons001", "pass", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
    # Test with invalid password (no uppercase)    
    def test_user_constructor_invalid_password_no_uppercase(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one uppercase letter"):
            newUser = User("Timmons001", "password", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
    # Test with invalid password (no lowercase)
    def test_user_constructor_invalid_password_no_lowercase(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one lowercase letter"):
            newUser = User("Timmons001", "PASSWORD", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
    # Test with invalid password (no number)
    def test_user_constructor_invalid_password_no_number(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one number"):
            newUser = User("Timmons001", "passworD", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
    # Test with invalid password (no special character)   
    def test_user_constructor_invalid_password_no_special_char(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one special character"):
            newUser = User("Timmons001", "Password1", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")     
    # Test with invalid password (contains space)
    def test_user_constructor_invalid_password_has_space(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password cannot contain spaces"):
            newUser = User("Timmons001", "P@ssw ord1", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid first name (not a string)
    def test_user_constructor_invalid_first_name_non_string(self):
        with self.assertRaises(TypeError, msg = "Name must be a string"):
            newUser = User("Timmons001", "P@ssword1", 123, "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid first name (empty string)
    def test_user_constructor_invalid_first_name_empty(self):
        with self.assertRaises(ValueError, msg = "Name cannot be empty"):
            newUser = User("Timmons001", "P@ssword1", "", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid first name (contains spaces)
    def test_user_constructor_invalid_first_name_contains_spaces(self):
        with self.assertRaises(ValueError, msg = "Name must contain only letters"):
            newUser = User("Timmons001", "P@ssword1", "Jac k", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid last name (not a string)
    def test_user_constructor_invalid_last_name_non_string(self):
        with self.assertRaises(TypeError, msg = "Name must be a string"):
            newUser = User("Timmons001", "P@ssword1", "Jack", 12345, "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid last name (empty string)
    def test_user_constructor_invalid_last_name_empty(self):
        with self.assertRaises(ValueError, msg = "Name cannot be empty"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid last name (contains spaces)
    def test_user_constructor_invalid_last_name_contains_spaces(self):
        with self.assertRaises(ValueError, msg = "Name must contain only letters"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Ti mmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer") 
    # Test with invalid DOB (not a string)
    def test_user_constructor_invalid_dob_non_string(self):
        with self.assertRaises(InvalidDOBError, msg = "DOB must be a string in the format MM/DD/YYYY"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", 12345, "jacktimmonsemail@gmail.com", "customer") 
    # Test with invalid DOB (empty string)
    def test_user_constructor_invalid_dob_empty(self):
        with self.assertRaises(InvalidDOBError, msg = "DOB must be a string in the format MM/DD/YYYY"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "", "jacktimmonsemail@gmail.com", "customer") 
    # Test with invalid DOB (invalid format)
    def test_user_constructor_invalid_dob_invalid_format(self):
        with self.assertRaises(InvalidDOBError, msg = "DOB must be a string in the format MM/DD/YYYY"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "1996-03-27", "jacktimmonsemail@gmail.com", "customer") 
            
             
    
            
             