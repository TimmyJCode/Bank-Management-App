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
    def __init__(self):
        pass

# The account class is the base class for the checking, savings, credit, and investment account classes
# Each account has an account ID, the user ID of the user that owns the account, the balance of the account,
# a list of transaction records, the date the account was created, and the status of the account.
class Account:
    def __init__(self, accountID: str, userID: str, balance: float, transactions: list[Transaction], dateCreated: date, status: str):
        pass