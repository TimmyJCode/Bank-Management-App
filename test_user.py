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
    def setUp(self):
        self.validUser = User("Timmons001", "J@cksPassword1234", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")
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
        with self.assertRaises(ValueError, msg = "Invalid Name: Name must be a string"):
            newUser = User("Timmons001", "P@ssword1", 123, "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid first name (empty string)
    def test_user_constructor_invalid_first_name_empty(self):
        with self.assertRaises(ValueError, msg = "Invalid Name: Name cannot be empty"):
            newUser = User("Timmons001", "P@ssword1", "", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid first name (contains spaces)
    def test_user_constructor_invalid_first_name_contains_spaces(self):
        with self.assertRaises(ValueError, msg = "Invalid Name: Name must contain only letters"):
            newUser = User("Timmons001", "P@ssword1", "Jac k", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "customer")  
    # Test with invalid last name (not a string)
    def test_user_constructor_invalid_last_name_non_string(self):
        with self.assertRaises(TypeError, msg = "Invalid Name: Name must be a string"):
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
    # Test with invalid DOB (user is too young)
    def test_user_constructor_invalid_dob_too_young(self):
        with self.assertRaises(InvalidDOBError, msg = "User must be at least 18 years old"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/2010", "jacktimmonsemail@gmail.com", "customer") 
    # Test with invalid email (not a string)
    def test_user_constructor_invalid_email_non_string(self):
        with self.assertRaises(TypeError, msg = "Email must be a string"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/2010", 12345, "customer")                             
    # Test with invalid email (empty string)
    def test_user_constructor_invalid_email_empty(self):
        with self.assertRaises(ValueError, msg = "Email cannot be empty"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/1996", "", "customer") 
    # Test with invalid email (invalid format)
    def test_user_constructor_invalid_email_invalid_format(self):
        with self.assertRaises(ValueError):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail", "customer")
    # Test with invalid role (not a string)
    def test_user_constructor_invalid_role_non_string(self):
        with self.assertRaises(TypeError, msg = "Role must be a string"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", 12345)
    # Test with invalid role (empty string)
    def test_user_constructor_invalid_role_empty(self):
        with self.assertRaises(ValueError, msg = "Role cannot be empty"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "")
    # Test with invalid role (invalid role)
    def test_user_constructor_invalid_role_invalid(self):
        with self.assertRaises(ValueError, msg = "Role must be either 'customer' or 'admin'"):
            newUser = User("Timmons001", "P@ssword1", "Jack", "Timmons", "03/27/1996", "jacktimmonsemail@gmail.com", "badrole")

    # Test the first name setter
    # Test with valid first name
    def test_first_name_setter_valid(self):
        # Change the user's first name
        self.validUser.firstName = "John"
        # Check that the first name was changed
        self.assertEqual(self.validUser.firstName, "John")
    # Test with invalid first name (not a string)
    def test_first_name_setter_invalid_non_string(self):
        with self.assertRaises(TypeError, msg = "Name must be a string"):
            self.validUser.firstName = 12345
    # Test with invalid first name (empty string)
    def test_first_name_setter_invalid_empty(self):
        with self.assertRaises(ValueError, msg = "Name cannot be empty"):
            self.validUser.firstName = ""   
    # Test with invalid first name (contains spaces)
    def test_first_name_setter_invalid_contains_spaces(self):
        with self.assertRaises(ValueError, msg = "Name must contain only letters"):
            self.validUser.firstName = "Joh n"

    # Test the last name setter
    # Test with valid last name
    def test_last_name_setter_valid(self):
        # Change the user's last name
        self.validUser.lastName = "Doe"
        # Check that the last name was changed
        self.assertEqual(self.validUser.lastName, "Doe")
    # Test with invalid last name (not a string)
    def test_last_name_setter_invalid_non_string(self):
        with self.assertRaises(TypeError, msg = "Name must be a string"):
            self.validUser.lastName = 12345
    # Test with invalid last name (empty string)
    def test_last_name_setter_invalid_empty(self):
        with self.assertRaises(ValueError, msg = "Name cannot be empty"):
            self.validUser.lastName = ""
    # Test with invalid last name (contains spaces)
    def test_last_name_setter_invalid_contains_spaces(self):
        with self.assertRaises(ValueError, msg = "Name must contain only letters"):
            self.validUser.lastName = "Do e"

    # Test the email setter
    # Test with valid email
    def test_email_setter_valid(self):
        # Change the user's email
        self.validUser.email = "jackNewEmail@yahoo.com"
        # Check that the email was changed
        self.assertEqual(self.validUser.email, "jackNewEmail@yahoo.com")
    # Test with invalid email (not a string)
    def test_email_setter_invalid_non_string(self):
        with self.assertRaises(TypeError, msg = "Email must be a string"):
            self.validUser.email = 12345
    # Test with invalid email (empty string) 
    def test_email_setter_invalid_empty(self):
        with self.assertRaises(ValueError, msg = "Email cannot be empty"):
            self.validUser.email = ""
    # Test with invalid email (invalid format)
    def test_email_setter_invalid_format(self):
        with self.assertRaises(ValueError):
            self.validUser.email = "jackNewEmail"
                        
    # Test the changePassword method
    # Test with valid password
    def test_change_password_valid(self):
        # Change the user's password
        self.validUser.changePassword("J@cksPassword1234", "J@cksNewPassword1234")
        # Check that the password was changed
        self.assertTrue(self.validUser.checkPassword("J@cksNewPassword1234"))        
    # Test with invalid password (incorrect old password)
    def test_change_password_invalid_incorrect_old_password(self):
        with self.assertRaises(InvalidPasswordError, msg = "Incorrect password"):
            self.validUser.changePassword("J@cksPassword12345", "J@cksNewPassword1234")
    # Test with invalid password (new password is invalid)
    def test_change_password_invalid_new_password(self):
        with self.assertRaises(InvalidPasswordError, msg = "Password must be at least 8 characters long"):
            self.validUser.changePassword("J@cksPassword1234", "pass")
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one uppercase letter"): 
            self.validUser.changePassword("J@cksPassword1234", "password")
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one lowercase letter"):
            self.validUser.changePassword("J@cksPassword1234", "PASSWORD")
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one number"):
            self.validUser.changePassword("J@cksPassword1234", "passworD")
        with self.assertRaises(InvalidPasswordError, msg = "Password must contain at least one special character"):
            self.validUser.changePassword("J@cksPassword1234", "Password1")
        with self.assertRaises(InvalidPasswordError, msg = "Password cannot contain spaces"):
            self.validUser.changePassword("J@cksPassword1234", "P@ssw ord1")        
        with self.assertRaises(TypeError, msg = "Password must be a string"):
            self.validUser.changePassword("J@cksPassword1234", 12345)
    
    # Test __str__ method
    def test_str(self):
        # Check that the string representation of the user is correct
        self.assertEqual(str(self.validUser), f"User ID: Timmons001\nName: Jack Timmons\nEmail: jacktimmonsemail@gmail.com\nRole: customer\nDOB: 03/27/1996")
