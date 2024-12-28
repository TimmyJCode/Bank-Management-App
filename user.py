# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain the class interface of the user class and its derived customer
# and admin classes

from datetime import datetime, date
from email_validator import validate_email, EmailNotValidError
from utilities import *
from errors import *


# The user class is the base class for the customer and admin classes, containing the basic information
# of a user of the bank management system
class User:
    # The constructor for the user class takes in the user's ID, raw password, and email
    def __init__(self, userID: str, rawPassword: str, firstName: str, lastName: str, DOB: str, email: str, role: str):
        # Check that the passed values are of the correct type
        if not isinstance(userID, str):
            raise TypeError("User ID must be a string")
        if not isinstance(role, str):
            raise TypeError("Role must be a string")
        # Check that the passed values are not empty
        if not userID.strip():
            raise ValueError("User ID cannot be empty") 
        if not role.strip():
            raise ValueError("Role cannot be empty")
        # Check that the role is valid
        if not isValidRole(role):
            raise ValueError("Invalid role")

        self._userID: str = userID 
        self._hashedPassword: str = self._hashPassword(rawPassword)
        self._email: str = email # Uses setter to check for valid email
        self._role: str = role 
        self._firstName: str = self._validateName(firstName) # Uses setter to check for valid first name
        self._lastName: str = self._validateName(lastName)  # Uses setter to check for valid last name
        self._DOB: date  = self._validateDOB(DOB) # Uses setter to check for valid DOB

    # Getter for the user's userID
    @property
    def userID(self) -> str:
        return self._userID  

    # Getter and setter for the user's first name
    @property
    def firstName(self) -> str:
        return self._firstName 
    @firstName.setter
    def firstName(self, newFirstName: str):
        self._firstName = self._validateName(newFirstName)

    # Getter and setter for the user's last name
    @property
    def lastName(self) -> str:
        return self._lastName
    @lastName.setter
    def lastName(self, newLastName: str):
        self._lastName = self._validateName(newLastName)
    
    # Getter and setter for the user's email
    @property
    def email(self) -> str:
        return self._email
    @email.setter
    def email(self, newEmail: str):
        if not isinstance(newEmail, str):
            raise TypeError("Email must be a string")
        if not newEmail.strip():
            raise ValueError("Email cannot be empty")
        self._email = newEmail
    
    # Getter for the user's date of birth
    @property
    def DOB(self) -> str:
        return self._DOB
    
    # Getter for the user's role
    @property
    def role(self) -> str:
        return self._role
    
    # Uses the PasswordService class to validate and hash the raw password- the hashed password is
    # returned as a hex string
    def _hashPassword(self, rawPassword: str) -> str:
        # Validate the password
        PasswordService.validatePassword(rawPassword)
        return PasswordService.hashPassword(rawPassword)
    
    # Allows the user to change their password, first checking the old password
    def changePassword(self, oldRawPassword: str, newRawPassword: str):
        if not self.checkPassword(oldRawPassword):
            raise InvalidPasswordError("Incorrect password")
        # Validate and hash the new password
        newHashedPassword = self._hashPassword(newRawPassword)
        self._hashedPassword = newHashedPassword

    # Checks if the passed raw password matches the hashed password
    def checkPassword(self, rawPassword: str) -> bool:
        return PasswordService.checkPassword(rawPassword, self._hashedPassword)
    
    # Validates the passed date of birth, ensuring it is a string in the format MM/DD/YYYY and that the
    # user is at least 18 years old
    def _validateDOB(self, DOB: str) -> date:
        # Ensure the passed date of birth is a string
        if not isinstance(DOB, str):
            raise InvalidDOBError("DOB must be a string in the format MM/DD/YYYY")
        # Attempt to parse the date of birth into a date object
        try:
            parsedDOB = datetime.strptime(DOB, "%m/%d/%Y").date()
        # If the date of birth is not in the correct format, raise an error
        except ValueError:
            raise InvalidDOBError("DOB must be a string in the format MM/DD/YYYY")
        # Ensure that the DOB is at least 18 years in the past (the minimum age for a user)
        today = date.today()
        if today.year - parsedDOB.year - ((today.month, today.day) < (parsedDOB.month, parsedDOB.day)) < 18:
            raise InvalidDOBError("User must be at least 18 years old")
        return parsedDOB
    
    # Validates the passed name, ensuring it is a string containing only letters
    def _validateName(self, name: str) -> str:
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if not name.strip():
            raise ValueError("Name cannot be empty")
        if not name.isalpha():
            raise ValueError("Name must contain only letters")
        return name

    # Validates the passed email, ensuring it is a string in a valid email format
    # using the email_validator library
    def _validateEmail(self, email: str) -> str:
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        if not email.strip():
            raise ValueError("Email cannot be empty")
        try:
          emailInfo = validate_email(email, check_deliverability=False)
          return emailInfo.normalized  
        except EmailNotValidError as e:
            raise ValueError(f"Invalid email addresss: {e}")
