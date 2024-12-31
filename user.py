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
from accounts import Account


# The user class is the base class for the customer and admin classes, containing the basic information
# of a user of the bank management system
class User:
    # The constructor for the user class takes in the user's ID, raw password, and email
    def __init__(self, userID: str, rawPassword: str, firstName: str, lastName: str, DOB: str, email: str, role: str):
        self._userID: str = self._validateUserID(userID) 
        self._hashedPassword: str = self._hashPassword(rawPassword)
        self._email: str = self._validateEmail(email) 
        self._role: str = self._validateRole(role) 
        self._firstName: str = self._validateName(firstName) 
        self._lastName: str = self._validateName(lastName)  
        self._DOB: date  = self._validateDOB(DOB) 

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
        email = self._validateEmail(newEmail) 
        self._email = email
    
    # Getter for the user's date of birth
    @property
    def DOB(self) -> str:
        return self._DOB
    
    # Getter for the user's role
    @property
    def role(self) -> str:
        return self._role

    # Validates the input userID, ensuring it is a non-empty string
    def _validateUserID(self, userID: str) -> str:
        if not isinstance(userID, str):
            raise TypeError("User ID must be a string")
        if not userID.strip():
            raise ValueError("User ID cannot be empty")
        return userID 
  
    # Uses the PasswordService class to validate and hash the raw password- the hashed password is
    # returned as a hex string
    def _hashPassword(self, rawPassword: str) -> str:
        # Validate the password
        PasswordService.validatePassword(rawPassword)
        return PasswordService.hashPassword(rawPassword)
    
    # Allows the user to change their password, first checking the old password
    def changePassword(self, oldRawPassword: str, newRawPassword: str) -> None:
        # Check the user's previous password
        if not self.checkPassword(oldRawPassword):
            raise InvalidPasswordError("Incorrect password")
        # Validate and hash the new password, set as the user's stored password
        PasswordService.validatePassword(newRawPassword)
        self._hashedPassword = self._hashPassword(newRawPassword)

    # Checks if the passed raw password matches the hashed password using the PasswordService class
    def checkPassword(self, rawPassword: str) -> bool:
        return PasswordService.checkPassword(rawPassword, self._hashedPassword)
    
    # Validates the passed date of birth, ensuring it is a non-empty string in the format MM/DD/YYYY and that the
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
    
    # Validates the passed name, ensuring it is a non-empty string containing only letters
    def _validateName(self, name: str) -> str:
        # Validate the name is a non-empty alphanumeric string
        try: name = validateAlnumString(name, "Name", 50)
        except InputError as e: raise ValueError(f"Invalid Name: {e}")
        return name

    # Validates the passed email, ensuring it is a non-empty string in a valid email format
    # using the email_validator library
    def _validateEmail(self, email: str) -> str:
        # Validate the the email is a non-empty string
        try: email = validateString(email, "Email", 100)
        except InputError as e: raise ValueError(f"Invalid email address: {e}")
        try:
          emailInfo = validate_email(email, check_deliverability=False)
          return emailInfo.normalized  
        except EmailNotValidError as e: raise ValueError(f"Invalid email addresss: {e}")
        
    # Validates the passed role, ensuring it is a string in the list of valid roles
    def _validateRole(self, role: str) -> str:
        if role not in VALID_ROLES:
            raise ValueError("Invalid role")
        return role    
   
    # Returns a string representation of the user, including their ID, name, email, role, and date of birth
    def __str__(self) -> str:
        return f"User ID: {self._userID}\nName: {self._firstName} {self._lastName}\nEmail: {self._email}\nRole: {self._role}\nDOB: {self._DOB.strftime("%m/%d/%Y")}"
    
# The customer class is a derived class of the user class, containing
# additional information specific to a customer of the bank management system
# and functionality for managing their accounts
class Customer(User):
    # The constructor for the customer class takes in the user's ID, raw password, email, and
    # additional information specific to a customer, as well as setting up the customer's dictionary
    # of accounts
    def __init__(self, userID: str, rawPassword: str, firstName: str, lastName: str, DOB: str, email: str):
        super().__init__(userID, rawPassword, firstName, lastName, DOB, email, "customer")
        # The customer class also includes a dictionary of the customer's accounts, indexed by account ID
        self._accounts: dict[str, Account] = {}
    
  