# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain custom error classes that are used throughout the program

class InvalidPasswordError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)


class InvalidDOBError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidAccountIDError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidInitialDepositError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidTransactionIDError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidTransactionAmountError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)

class InvalidTransactionTypeError(ValueError):
    def __init__(self, message: str):
        super().__init__(message)