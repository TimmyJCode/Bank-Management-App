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
    def __init__(self, userID: str, accountID: str, amount: float, transactionType: str, description: str = None,
                  origin: str = None, fee: float = 0.00):
        # Time Stamp: The date and time the transaction was made
        self._timeStamp = datetime.now()
        # User ID: The ID of the user that made the transaction
        self._userID: str = userID
        # Account ID: The ID of the account that the transaction was made on
        self._accountID: str = accountID
        # Amount: The floating point amount of the transaction
        self._amount: float = self._validateAmount(amount)
        # Transaction Type: The type of the transaction- list of acceptable transaction types in utilities.py
        self._transactionType: str = self._validateTransactionType(transactionType)
        # Fee: The fee charged for the transaction (default is 0.00)
        self._fee = self._validateFee(fee)
        # Origin: The origin of the transaction (if supplied)
        self._origin = self._validateOrigin(origin) if origin else None
        # Description: A description of the transaction (if supplied)
        self._description = self._validateDescription(description) if description else None
        # Transaction ID: A unique alphanumeric string that identifies the transaction
        # Transaction ID format: userID-transactionType-timeStamp.isoformat()
        # The stored transaction ID is hashed using bcrypt for security
        self._transactionID: str = self._generateTransactionID()

    # Getter for the transaction ID
    @property
    def transactionID(self) -> str:
        return self._transactionID
    
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
    
    # Getter for the transaction type
    @property
    def transactionType(self) -> str:
        return self._transactionType
    
    # Getter for the fee
    @property
    def fee(self) -> float:
        return self._fee
    
    # Getter for the origin
    @property
    def origin(self) -> str:
        return self._origin
    
    # Getter for the description
    @property
    def description(self) -> str:
        return self._description
    
    # Getter for the time stamp
    @property
    def timeStamp(self) -> datetime:
        return self._timeStamp

    # Validates that the userID, transactionType, and timeStamp are present in the transaction
    # object at time of transaction ID creation- throws a transaction error if any of the metadata
    # is missing
    def _validateTransactionMetadata(self) -> None:
        if not self._userID:
            raise TransactionError("User ID is required to generate a transaction ID")
        if not self._transactionType:
            raise TransactionError("Transaction type is required to generate a transaction ID")
        if not self._timeStamp:
            raise TransactionError("Time stamp is required to generate a transaction ID")

    # Generates a unique transaction ID for the transaction object- the transaction ID is a string
    # in the format userID-transactionType-timeStamp.isoformat(), hashed using bcrpyt 
    def _generateTransactionID(self) -> str:
        # Validate that the transaction metadata is present
        self._validateTransactionMetadata()
        # Metadata string format: userID-transactionType-timeStamp.isoformat()
        metaData: str = f"{self._userID}-{self._transactionType}-{self._timeStamp.isoformat()}"
        # Hash the metadata string using bcrypt
        return bcrypt.hash(metaData.encode())

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
            raise InvalidTransactionTypeError("Invalid Transaction Type")
        return transactionType
    
    # Ensures that the fee is a non-negative floating point number- if the fee is negative, throws a DepositError
    def _validateFee(self, fee: float) -> float:
        if not isinstance(fee, float):
            raise TransactionError("Fee must be a floating point number")
        if fee < 0:
            raise TransactionError("Fee must be greater than or equal to 0")
        return fee

    # Ensures that the origin is a non-empty string- if the origin is empty or non alpha-numeric,
    # throws a DepositError
    def _validateOrigin(self, origin: str) -> str:
        if not isinstance(origin, str) and origin is not None:
            raise TransactionError("Origin must be a string")
        return origin
 
    # Ensures that the description is a non-empty string- if the description is empty or non alpha-numeric,
    # throws a TransactionError
    def _validateDescription(self, description: str) -> str:
        if not isinstance(description, str) and description is not None:
            raise TransactionError("Description must be a string")
        return description
    
    # Returns a string representation of the transaction object
    def __str__(self):
        return f"Transaction ID: {self._transactionID}\nUser ID: {self._userID}\nAccount ID: {self._accountID}\nAmount: {self.amount}\nTransaction Type: {self.transactionType}"
    
# The deposit class is a subclass of the transaction class, and is used to represent a deposit transaction
# in the bank management system
# Each deposit has a transaction ID, the user ID of the user that made the deposit, the account ID of the account
# that the deposit was made on, the amount of the deposit, the type of transaction (deposit), and the date and time of the deposit
class Deposit(Transaction):
    # The constructor for the deposit class takes in the user ID, account ID, and amount of the deposit, and initializes
    # the deposit with the given values after validating that the amount is a valid floating point number
    def __init__(self, userID: str, accountID: str, amount: float, depositMethod: str, fee: float = 0.00,
                 transactionType: str = "Deposit", origin: str = None, description: str = None):
        # Call the Transaction class constructor
        super().__init__(userID, accountID, amount, transactionType, description, origin, fee)
        # Deposit Method: The method used to make the deposit
        self._depositMethod: str = self._validateDepositMethod(depositMethod)
        
    # Getter for the deposit method
    @property
    def depositMethod(self) -> str:
        return self._depositMethod
    
    # Ensures that the deposit method is a valid deposit method as defined in the utilities.py file
    # If deposit method is invalid, throws DepositError exception
    def _validateDepositMethod(self, depositMethod: str) -> str:
        if depositMethod not in VALID_DEPOSIT_METHODS:
            raise DepositError("Invalid deposit method")
        return depositMethod
    
    
   


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
    
    # Setter for the status- ensures the status is a valid account status
    @status.setter
    def status(self, newStatus: str):
        # Verify status is within the list of valid statuses
        if newStatus not in VALID_STATUSES:
            raise ValueError("Status must be 'Active', 'Frozen', or 'Closed'")
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
    
 