# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain the test interface for the account, checking, savings, credit,
# investment, and transaction classes

import unittest
import pytest
from datetime import datetime, date
from unittest.mock import patch
from user import *
from utilities import *
from accounts import *
from errors import *

# Test Transaction class
class TestTransaction(unittest.TestCase):
    # Fixture representing valid account object
    @pytest.fixture
    def validAccount(self):
        return Account("Timm0001", "TimmonsJ1996", 1000.00)

    # Test Account Constructor:
    # Test constructor with valid values
    def test_account_constructor_valid(self, accountID = "Timm0001", userID = "TimmonsJ1996", initialDeposit = 1000.00):
        account = Account(accountID, userID, initialDeposit)
        self.assertEqual(account.accountID, accountID)
        self.assertEqual(account.userID, userID)
        self.assertEqual(account.balance, initialDeposit)
        self.assertEqual(account.dateCreated, date.today())
        self.assertEqual(account.status, "Active")
        self.assertEqual(account.transactions, [])
    # Test constructor with invalid (non-string) account ID
    def test_account_constructor_invalid_accountID_non_string(self):
        with self.assertRaises(InvalidAccountIDError, msg = "Account ID must be a string"):
            Account(100, "TimmonsJ1996", 1000.00)
    # Test constructor with invalid (non-alphanumeric) account ID
    def test_account_constructor_invalid_accountID_non_alphanumeric(self):
        with self.assertRaises(InvalidAccountIDError, msg = "Account ID must be alphanumeric"):
            Account("Timm-0001", "TimmonsJ1996", 1000.00)
    # Test constructor with invalid (empty string) account ID 
    def test_account_constructor_invalid_accountID_empty_string(self):
        with self.assertRaises(InvalidAccountIDError, msg = "Account ID cannot be an empty string"):
            Account("", "TimmonsJ1996", 1000.00)
    # Test constructor with invalid (non-floating point) initial deposit
    def test_account_constructor_invalid_initial_deposit_non_float(self):
        with self.assertRaises(InvalidInitialDepositError, msg = "Initial deposit must be a floating point number"):
            Account("Timm0001", "TimmonsJ1996", "1000.00")
    # Test constructor with invalid (negative) initial deposit
    def test_account_constructor_invalid_initial_deposit_negative(self):
        with self.assertRaises(InvalidInitialDepositError, msg = "Initial deposit must be greater than or equal to 0"):
            Account("Timm0001", "TimmonsJ1996", -1000.00)

