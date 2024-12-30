# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain the class interfaces of the account, checking, savings, credit,
# investment, and transaction classes

from datetime import datetime, date
from utilities import *
from errors import *

# The transaction class is used to represent a transaction record in the bank management system
# Each transaction has a transaction ID, the user ID of the user that made the transaction, the account
# ID of the account that the transaction was made on, the amount of the transaction, the type of the
# transaction, and the date and time of the transaction. 
class Transaction:
    # The constructor for the transaction class takes in the transaction ID, user ID, account ID, amount, and
    # transaction type, and initializes the transaction with the given values after validating that the transaction
    # ID is valid, the amount is a floating point number, and the transaction type is a valid type
    def __init__(self, transactionID: str, userID: str, accountID: str, amount: float, transactionType: str):
        self._transactionID: str = self._validateTransactionID(transactionID)
        self._userID: str = userID
        self._accountID: str = accountID
        self._amount: float = self._validateAmount(amount)
        self._transactionType: str = self._validateTransactionType(transactionType)

    # Getter for the transaction ID
    @property
    def transactionID(self) -> str:
        return self._transactionID
    
    # Setter for the transaction ID- ensures the transaction ID is a non-empty alphanumeric string
    @transactionID.setter
    def transactionID(self, newTransactionID: str):
        self._transactionID = self._validateTransactionID(newTransactionID)
    
    # Getter for the user ID
    @property
    def userID(self) -> str:
        return self._userID
    
    # Getter for the account ID
    @property
    def accountID(self) -> str:
        return self._accountID
    
    # Getter for the amount
    @property
    def amount(self) -> float:
        return self._amount
    
    # Setter for the amount- ensures the amount is a floating point number
    @amount.setter
    def amount(self, newAmount: float):
        self._amount = self._validateAmount(newAmount)
    
    # Getter for the transaction type
    @property
    def transactionType(self) -> str:
        return self._transactionType
    
    # Ensures the transaction ID is a non-empty alphanumeric string- throws an
    # invalid transaction ID error if the transaction ID is not a string, is empty,
    # or is not alphanumeric
    def _validateTransactionID(self, transactionID: str) -> str:
        if not isinstance(transactionID, str):
            raise InvalidTransactionIDError("Transaction ID must be a string")
        if not transactionID:
            raise InvalidTransactionIDError("Transaction ID cannot be empty")
        if not transactionID.isalnum():
            raise InvalidTransactionIDError("Transaction ID must be alphanumeric")
        return transactionID

    # Validates that the amount of the transaction is a floating point number- throws
    # a value error exception if the amount is not a float
    def _validateAmount(self, amount: float) -> float:
        if not isinstance(amount, float):
            raise InvalidTransactionAmountError("Amount must be a floating point number")
        return amount

    # Ensures that the transaction type is a non-empty string and is a valid transaction type- throws 
    # an invalid transaction type error if the transaction type is not a string, is empty, or is not a valid
    # transaction type
    def _validateTransactionType(self, transactionType: str) -> str:
        if not isinstance(transactionType, str):
            raise InvalidTransactionTypeError("Transaction type must be a string")
        if not transactionType:
            raise InvalidTransactionTypeError("Transaction type cannot be empty")
        if transactionType not in VALID_TRANSACTION_TYPES:
            raise InvalidTransactionTypeError("Transaction type must be either 'Deposit' or 'Withdrawal'")
        return transactionType
    
    # Returns a string representation of the transaction object
    def __str__(self):
        return f"Transaction ID: {self.transactionID}\nUser ID: {self.userID}\nAccount ID: {self.accountID}\nAmount: {self.amount}\nTransaction Type: {self.transactionType}"

# The account class is the base class for the checking, savings, credit, and investment account classes
# Each account has an account ID, the user ID of the user that owns the account, the balance of the account,
# a list of transaction records, the date the account was created, and the status of the account.
class Account:
    # The constructor for the account class takes in the account ID, user ID, and initial deposit, 
    # and initializes the account with the given values after validating that the account ID and initial
    # deposit are valid
    def __init__(self, accountID: str, userID: str, initialDeposit: float):
        # Account ID: The first 4 digits of the UserID, followed by the a 4 digit number starting at 0001
        # for all accounts in the simulated banking system
        self._accountID: str = self._validateAccountID(accountID)
        # User ID: The ID of the user that owns the account
        self._userID: str = userID
        # Balance: The balance of the account, initialized to the initial deposit provided at the time
        # of account creation
        self._balance : float = self._validateInitialDeposit(initialDeposit)
        # Transactions: A list of transaction records for the account
        self._transactions: list[Transaction] = []
        self._dateCreated: date = date.today()
        self._status: str = "Active"

    # Getter for the account ID
    @property
    def accountID(self) -> str:
        return self._accountID
    
    # Getter for the user ID
    @property
    def userID(self) -> str:
        return self._userID
    
    # Getter for the balance
    @property
    def balance(self) -> float:
        return self._balance
    
    # Getter for the transactions
    @property
    def transactions(self) -> list[Transaction]:
        return self._transactions
    
    # Getter for date created
    @property
    def dateCreated(self) -> date:
        return self._dateCreated
    
    # Getter for the status
    @property
    def status(self) -> str:
        return self._status
    
    # Setter for the status- ensures the status is a non-empty string and is a valid account status
    @status.setter
    def status(self, newStatus: str):
        # Verify status is a string
        if not isinstance(newStatus, str):
            raise TypeError("Status must be a string")
        # Verify status is not empty
        if not newStatus:
            raise ValueError("Status cannot be empty")
        # Verify status is within the list of valid statuses
        if newStatus not in VALID_STATUSES:
            raise ValueError("Status must be either 'Active' or 'Closed'")
        self._status = newStatus
    
    # Validates that the account ID is a non empty string
    def _validateAccountID(self, accountID: str) -> str:
        # Check that the account ID is a string
        if not isinstance(accountID, str):
            raise InvalidAccountIDError("Account ID must be a string")
        # Check that the account ID is not empty
        if not accountID:
            raise InvalidAccountIDError("Account ID cannot be empty")
        # Check that the account ID is alphanumeric
        if not accountID.isalnum():
            raise InvalidAccountIDError("Account ID must be alphanumeric")
        return accountID

    # Validates that the intial balance allocated to an account is a non-negative float 
    def _validateInitialDeposit(self, deposit: float) -> float:
        # Check that the balance is a float
        if not isinstance(deposit, float):
            raise InvalidInitialDepositError("Initial deposit must be a floating point number")
        # Check that the deposit is greater than or equal to 0
        if deposit < 0:
            raise InvalidInitialDepositError("Initial deposit must be greater than or equal to 0")
        return deposit

    # Returns a string representation of the account object 
    def __str__(self) -> str:
        return f"Account ID: {self.accountID}\nUser ID: {self.userID}\nBalance: {self.balance}\nDate Created: {self.dateCreated}\nStatus: {self.status}\nTransactions: {self.transactions}"
    
 