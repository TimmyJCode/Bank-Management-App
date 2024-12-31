# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain reusable utility functions that are used throughout the program


from passlib.hash import bcrypt
from errors import *

# List of valid user roles, for checks in the user constructor
VALID_ROLES: list[str] = ["customer", "admin"]
# List of valid account statuses, for checks in the account status setter
VALID_STATUSES: list[str] = ["Active", "Frozen", "Closed"]
# List of valid transaction types, for checks in the transaction type setter
VALID_TRANSACTION_TYPES: list[str] = ["Deposit", "Withdrawal", "Intra-Transfer", "External-Transfer"]
# List of valid deposit methods
VALID_DEPOSIT_METHODS: list[str] = ["Cash", "Check", "Wire", "Transfer", "Direct-Deposit", "Mobile-Deposit"]
# List of valid withdrawal methods
VALID_WITHDRAWAL_METHODS: list[str] = ["Cash", "Check", "Wire", "Transfer"]


# Determines if the passed string (such as a description or origin) is a string of less than
# maxLength characters- if the optional flag is set to true, the string can be empty
def validateString(value: str, valueName: str, maxLength: int, optional: bool = False) -> str:
    # Check if the passed value is a string
    if not isinstance(value, str):
        raise InputError(f"{valueName} must be a string")
    # Check if the value is empty
    if not value:
        if optional:
            return value
        else:
            raise InputError(f"{valueName} cannot be empty")
    # Check if the value is too long
    elif len(value) > maxLength:
        raise InputError(f"{valueName} must be less than {maxLength} characters long")
    return value

# Determines if the passed string is a non-empty string of less than maxLength characters (if optional is set to true)
# If the string fails validation, an InputError is raised
def validateAlnumString(value: str, valueName: str, maxLength: int, optional: bool = False) -> str:
    # Check if the passed value is a string
    if not isinstance(value, str):
        raise InputError(f"{valueName} must be a string")
    # Check if the value is empty
    if not value:
        if optional:
            return value
        else:
            raise InputError(f"{valueName} cannot be empty")
    # Check if the value is too long
    elif len(value) > maxLength:
        raise InputError(f"{valueName} must be less than {maxLength} characters long")
    # Check if the value is alphanumeric
    elif not value.isalnum():
        raise InputError(f"{valueName} must be alphanumeric")
    return value

# Determines if the passed value is a positive float, and raises an InputError if it is not
def validatePositiveFloat(value: float, valueName: str) -> float:
    # Check if the passed value is a float
    if not isinstance(value, float):
        raise InputError(f"{valueName} must be a floating point number")
    # Check if the value is positive
    if value <= 0:
        raise InputError(f"{valueName} must be greater than or equal to 0")
    return value
    

# Class PasswordService will manage the hasing, checking, and verification of passwords
class PasswordService:
    # Hash the passed password string using bcrypt and returns a hex string
    @staticmethod
    def hashPassword(rawPassword: str) -> str:
        return bcrypt.hash(rawPassword.encode())
    
    # Check if the passed password matches the hashed password
    @staticmethod
    def checkPassword(rawPassword: str, hashedPassword: str) -> bool:
        return bcrypt.verify(rawPassword.encode(), hashedPassword)
    
    # Check if the passed password is a valid password based on the following criteria:
    # - At least 8 characters long
    # - Contains at least one uppercase letter
    # - Contains at least one lowercase letter
    # - Contains at least one number
    # - Contains at least one special character
    # - Contains no spaces
    @staticmethod
    def validatePassword(Password: str) -> None:
        # Validate that the passed password is a non-empty string
        if not isinstance(Password, str):
            raise TypeError("Password must be a string")
        # Check length
        if len(Password) < 8:
            raise InvalidPasswordError("Password must be at least 8 characters long")
        # Check for uppercase letter
        if not any(char.isupper() for char in Password):
            raise InvalidPasswordError("Password must contain at least one uppercase letter")
        # Check for lowercase letter
        if not any(char.islower() for char in Password):
            raise InvalidPasswordError("Password must contain at least one lowercase letter")
        # Check for number
        if not any(char.isdigit() for char in Password):
            raise InvalidPasswordError("Password must contain at least one number")
        # Check for special character
        if not any(not char.isalnum() and not char.isspace() for char in Password):
            raise InvalidPasswordError("Password must contain at least one special character")
        # Check for spaces
        if any(char.isspace() for char in Password):
            raise InvalidPasswordError("Password cannot contain spaces")