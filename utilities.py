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

# Determines if the passed role is in the list of valid roles
def isValidRole(role: str) -> bool:
    return role in VALID_ROLES

# Class PasswordService will manage the hasing, checking, and verification of passwords
class PasswordService:
    # Hash the passed password string using bcrypt and returns a hex string
    @staticmethod
    def hashPassword(rawPassword: str) -> str:
        return bcrypt.hash(rawPassword)
    
    # Check if the passed password matches the hashed password
    @staticmethod
    def checkPassword(rawPassword: str, hashedPassword: str) -> bool:
        return bcrypt.verify(rawPassword, hashedPassword)
    
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