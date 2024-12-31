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
            raise TransactionError("Transaction Error: User ID is required to generate a transaction ID")
        if not self._transactionType:
            raise TransactionError("Transaction Error: Transaction type is required to generate a transaction ID")
        if not self._timeStamp:
            raise TransactionError("Transaction Error: Time stamp is required to generate a transaction ID")

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
    # a transaction error exception if the amount is not a float
    def _validateAmount(self, amount: float) -> float:
        if not isinstance(amount, float):
            raise TransactionError("Transaction Error: Amount must be a floating point number")
        return amount

    # Ensures that the transaction type is a non-empty string and is a valid transaction type- throws 
    # an invalid transaction type error if the transaction type is not a string, is empty, or is not a valid
    # transaction type
    def _validateTransactionType(self, transactionType: str) -> str:
        # Validate the transactionType string
        try: transactionType = validateString(transactionType, "Transaction Type", 50, False)
        except InputError as e: raise TransactionError(f"Transaction Error: {e}")
        if transactionType not in VALID_TRANSACTION_TYPES:
            raise TransactionError("Transaction Error: Invalid Transaction Type")
        return transactionType
    
    # Ensures that the fee is a non-negative floating point number- if the fee is negative, throws a TransactionError
    def _validateFee(self, fee: float) -> float:
        if not isinstance(fee, float):
            raise TransactionError("Transaction Erorr: Fee must be a floating point number")
        if fee < 0:
            raise TransactionError("Transaction Error: Fee must be greater than or equal to 0")
        return fee

    # Ensures that the origin is a non-empty string- if the origin is empty or non alpha-numeric,
    # throws a TransactionError
    def _validateOrigin(self, origin: str) -> str:
        try: origin = validateString(origin, "Origin", 50, True)
        except InputError as e: raise TransactionError(f"Transaction Error: {e}")
        return origin
 
    # Ensures that the description is a non-empty string- if the description is empty or non alpha-numeric,
    # throws a TransactionError
    def _validateDescription(self, description: str) -> str:
        try: description = validateString(description, "Description", 100, True)
        except InputError as e: raise TransactionError(f"Transaction Error: {e}")
        return description
    
    # Ensures that the destination account ID is a non-empty string, is alphanumeric, and is not the same as the source account ID
    # For use in transfer transactions
    def _validateDestinationAccountID(self, destinationAccountID: str) -> str:
        # Validate that destinationAccountID is a non-empty alphanumeric string
        try: destinationAccountID = validateAlnumString(destinationAccountID, "Destination Account ID", 50, False)
        except InputError as e: raise TransferError(f"Transfer Error: {e}")
        # Ensure destinationAccountID is not the same as the source account ID
        if destinationAccountID == self._accountID:
            raise TransferError("Transfer Error: Destination Account ID cannot be the same as the source account ID")
        return destinationAccountID

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
            raise DepositError("Deposit Error: Invalid deposit method")
        return depositMethod

    # Returns a string representation of the deposit object
    def __str__(self):
        return super().__str__() + f"\nDeposit Method: {self.depositMethod}"

# The withdrawal class is a subclass of the transaction class, and is used to represent a withdrawal transaction in
# the bank management system
# Each withdrawal has a transaction ID, the user ID of the user that made the withdrawal, the account ID of the account
# that the withdrawal was made on, the amount of the withdrawal, the type of transaction (withdrawal), and the date and time of the withdrawal
class Withdrawal(Transaction):
    # The constructor for the withdrawal class takes in the user ID, account ID, and amount of the withdrawal, as well as optional
    # information like fee (defaults to 0.00), origin, and description, and initializes the withdrawal with the given values
    # after validating the passed data
    def __init__(self, userID: str, accountID: str, amount: float, withdrawalMethod: str, fee: float = 0.00,
                 transactionType: str = "Withdrawal", origin: str = None, description: str = None):
        # Call the Transaction class constructor
        super().__init__(userID, accountID, amount, transactionType, description, origin, fee)
        # Withdrawal Method: The method used to make the withdrawal
        self._withdrawalMethod: str = self._validateWithdrawalMethod(withdrawalMethod)
    
    # Getter for the withdrawal method
    @property
    def withdrawalMethod(self) -> str:
        return self._withdrawalMethod

    # Ensures that the withdrawal method is a valid withdrawal method as defined in the utilities.py file
    # If withdrawal method is invalid, throws WithdrawalError exception
    def _validateWithdrawalMethod(self, withdrawalMethod: str) -> str:
        if withdrawalMethod not in VALID_WITHDRAWAL_METHODS:
            raise WithdrawalError("Withdrawal Error: Invalid withdrawal method")
        return withdrawalMethod
    
    # Returns a string representation of the withdrawal object
    def __str__(self):
        return super().__str__() + f"\nWithdrawal Method: {self.withdrawalMethod}"

# The transfer class is a subclass of the transaction class, and is used to represent a transfer transaction between two accounts in the bank
# management system
# Each transfer has a transaction ID, the user ID of the user that made the transfer, the account ID of the account that the transfer
# was made from, the account ID of the account that the transfer was made to (destination), the amount of the transfer, 
# the type of transaction (which must be "Intra-Transfer" or "External-Transfer"), the date and time of the transfer, and optional
# information like fee, origin, and description
class InternalTransfer(Transaction):
    def __init__(self, userID: str, accountID: str, destinationAccountID: str, amount: float, transactionType: str = "Intra-Transfer",
                 fee: float = 0.00, origin: str = None, description: str = None):
        # Call the Transaction class constructor
        super().__init__(userID, accountID, amount, transactionType, description, origin, fee)
        # Destination Account ID: The account ID of the account that the transfer is being made to
        self._destinationAccountID: str = self._validateDestinationAccountID(destinationAccountID)
    
    # Getter for the destination account ID
    @property
    def destinationAccountID(self) -> str:
        return self._destinationAccountID

    def __str__(self):
        return super().str() + f"\nDestination Account ID: {self._destinationAccountID}"

class ExternalTransfer(Transaction):
    def __init__(self, userID: str, accountID: str, destinationAccountID: str, destinationRoutingNumber: str, destinationBank:str, 
                 amount: float, transactionType: str = "External-Transfer", fee: float = 0.00, origin: str = None, description: str = None):
        # Call the Transaction class constructor
        super().__init__(userID, accountID, amount, transactionType, description, origin, fee)
        # Destination Account ID: The account ID of the account that the transfer is being made to
        self._destinationAccountID: str = self._validateDestinationAccountID(destinationAccountID)
        # Destination Routing Number: The routing number of the destination bank
        self._destinationRoutingNumber: str = self._validateDestinationRoutingNumber(destinationRoutingNumber)
        # Destination Bank: The name of the destination bank
        self._destinationBank: str = self._validateDestinationBank(destinationBank)

    # Ensures that the destination routing number is a 9 digit numeric string 
    def _validateDestinationRoutingNumber(self, destinationRoutingNumber: str) -> str:
        if not isinstance(destinationRoutingNumber, str):
            raise TransferError("Transfer Error: Destination Routing Number must be a string")
        if len(destinationRoutingNumber) != 9:
            raise TransferError("Transfer Error: Destination Routing Number must be 9 digits")
        if not destinationRoutingNumber.isnumeric():
            raise TransferError("Transfer Error: Destination Routing Number must be numeric")
        return destinationRoutingNumber
    
    # Ensures that the destination bank is a non-empty string
    def _validateDestinationBank(self, destinationBank: str) -> str:
        # Ensure the destinationBank is a non-empty string
        try: destinationBank = validateString(destinationBank, "Destination Bank", 50, False)
        except InputError as e: raise TransferError(f"Transfer Error: {e}")
        return destinationBank
    
    def __str__(self):
        return super().__str__() + f"\nDestination Account ID: {self._destinationAccountID}\nDestination Routing Number: {self._destinationRoutingNumber}\nDestination Bank: {self._destinationBank}"
    
   


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
        # Check that the accountID is a non-empty alphanumeric string
        try: accountID = validateAlnumString(accountID, "Account ID", 50, False)
        except InputError as e: raise AccountError(f"Account ID Error: {e}")
        return accountID

    # Validates that the intial balance allocated to an account is a non-negative float 
    def _validateInitialDeposit(self, deposit: float) -> float:
        # Check that the deposit is a positive float
        try: deposit = validatePositiveFloat(deposit, "Initial Deposit")
        except InputError as e: raise DepositError(f"Initial Deposit Error: {e}")
        return deposit

    # The makeDeposit method is used to add funds to the account balance
    # The method takes in the user ID of the user making the deposit, the amount of the deposit, the deposit method,
    # the fee charged for the deposit (default is 0.00), the origin of the deposit (default is None), and a description
    # of the deposit (default is None) 
    # The method creates a new deposit record, adds the deposit to the account's transaction list, and updates the account balance
    def makeDeposit(self, userID: str, amount: float, depositMethod: str, fee: float = 0.00, origin: str = None, description: str = None) -> None:
        # Ensure the account is active
        if not self.isActive():
            raise AccountError("Account Error: Account is not active")
        # Create a new deposit record
        deposit = Deposit(userID, self._accountID, amount, depositMethod, fee, origin, description)
        # Add the deposit to the account's transaction list
        self._transactions.append(deposit)
        # Update the account balance
        self._balance += amount
    
    # The makeWithdrawal method is used to remove funds from the account balance
    # The method takes in the user ID of the user making the withdrawal, the amount of the withdrawal, the withdrawal method,
    # the fee charged for the withdrawal (default is 0.00), the origin of the withdrawal (default is None), and a description
    # of the withdrawal (default is None)
    # The method creates a new withdrawal record, adds the withdrawal to the account's transaction list, and updates the account balance
    def makeWithdrawal(self, userID: str, amount: float, withdrawalMethod: str, fee: float = 0.00, origin: str = None, description: str = None) -> None:
        # Ensure the account is active
        if not self.isActive():
            raise AccountError("Account Error: Account is not active")
        # Ensure the withdrawal amount is less than the account balance
        if amount > self._balance:
            raise WithdrawalError("Withdrawal Error: Withdrawal amount exceeds account balance")
        # Create a new withdrawal record
        withdrawal = Withdrawal(userID, self._accountID, amount, withdrawalMethod, fee, origin, description)
        # Add the withdrawal to the account's transaction list
        self._transactions.append(withdrawal)
        # Update the account balance
        self._balance -= amount

    def isActive(self) -> bool:
        return self._status == "Active"

    # Returns a string representation of the account object 
    def __str__(self) -> str:
        return f"Account ID: {self.accountID}\nUser ID: {self.userID}\nBalance: {self.balance}\nDate Created: {self.dateCreated}\nStatus: {self.status}\nTransactions: {self.transactions}"
    