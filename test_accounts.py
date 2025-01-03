# Jack Timmons, 27 Dec 2024, Winter Break 
# The purpose of this program is to provide users with a simulated bank managment interface, gaining 
# expierence with OOP, full-stack development, and my first expierence creating both a local GUI and
# web-based application

# The purpose of this file is to contain the test interface for the account, checking, savings, credit,
# investment, and transaction classes

import unittest
import pytest
from passlib.hash import bcrypt
from datetime import datetime, date
from unittest.mock import patch
from user import *
from utilities import *
from accounts import *
from errors import *


# Test Transaction class
class TestTransaction(unittest.TestCase):
    # Set up valid values for testing
    def setUp(self):
        self.validAccount = Account("Timm0001", "TimmonsJ1996", 1000.00)
        self.validUserID = "TimmonsJ1996"
        self.validAccountID = "Timm0001"
        self.validAmount = 100.00
        self.validTransactionType = "Deposit"
        self.validFee = 1.00
        self.validOrigin = "XYZ Corporation"
        self.validDescription = "Payroll"

    # Test Transaction Constructor:
    # Test constructor with valid values (all values supplied)
    def test_transaction_constructor_valid(self):
        transaction = Transaction(self.validUserID, self.validAccountID, self.validAmount, self.validTransactionType, self.validDescription, self.validOrigin, self.validFee)
        self.assertEqual(transaction.userID, self.validUserID)
        self.assertEqual(transaction.accountID, self.validAccountID)
        self.assertEqual(transaction.amount, self.validAmount)
        self.assertEqual(transaction.transactionType, self.validTransactionType)
        self.assertEqual(transaction._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + transaction._timeStamp.isoformat()).encode(), transaction.transactionID))
        self.assertEqual(transaction.description, self.validDescription)
        self.assertEqual(transaction.origin, self.validOrigin)
        self.assertEqual(transaction.fee, self.validFee)
    # Test constructor with valid values (no fee, origin, or description)
    def test_transaction_constructor_valid_no_fee_origin_description(self):
        transaction = Transaction(self.validUserID, self.validAccountID, self.validAmount, self.validTransactionType)
        self.assertEqual(transaction.userID, self.validUserID)
        self.assertEqual(transaction.accountID, self.validAccountID)
        self.assertEqual(transaction.amount, self.validAmount)
        self.assertEqual(transaction.transactionType, self.validTransactionType)
        self.assertEqual(transaction._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + transaction._timeStamp.isoformat()).encode(), transaction.transactionID))
        self.assertIsNone(transaction.description)
        self.assertIsNone(transaction.origin)
        self.assertEqual(transaction.fee, 0.00)
    # Test constructor with invalid (non-float) amount
    def test_transaction_constructor_invalid_amount_non_float(self):
        with self.assertRaises(TransactionError, msg = "Amount must be a floating point number"):
            Transaction(self.validUserID, self.validAccountID, "100.00", self.validTransactionType)
    # Test with invalid transaction type
    def test_transaction_constructor_invalid_transaction_type(self):
        with self.assertRaises(TransactionError, msg = "Invalid transaction type"):
            Transaction(self.validUserID, self.validAccountID, self.validAmount, "Invalid")
    # Test with invalid (non-string) transaction type
    def test_transaction_constructor_invalid_transaction_type_non_string(self):
        with self.assertRaises(TransactionError, msg = "Transaction type must be a string"):
            Transaction(self.validUserID, self.validAccountID, self.validAmount, 100.00)
    # Test with invalid (empty string) transaction type
    def test_transaction_constructor_invalid_transaction_type_empty_string(self):
        with self.assertRaises(TransactionError, msg = "Transaction type cannot be an empty string"):
            Transaction(self.validUserID, self.validAccountID, self.validAmount, "")
    # Test with empty string for user ID
    def test_transaction_constructor_invalid_userID_empty_string(self):
        with self.assertRaises(TransactionError, msg = "User ID is required to generate a transaction ID"):
            Transaction("", self.validAccountID, self.validAmount, self.validTransactionType)

# Test Deposit class
class TestDeposit(TestTransaction):
    # Set up valid values for testing
    def setUp(self):
        super().setUp()
        self.validDepositMethod = "Direct-Deposit"

    # Test Deposit Constructor:
    # Test constructor with valid values (all values supplied)
    def test_deposit_constructor_valid(self):
        deposit = Deposit(self.validUserID, self.validAccountID, self.validAmount, self.validDepositMethod, self.validFee, self.validTransactionType, self.validOrigin, self.validDescription)
        self.assertEqual(deposit.userID, self.validUserID)
        self.assertEqual(deposit.accountID, self.validAccountID)
        self.assertEqual(deposit.amount, self.validAmount)
        self.assertEqual(deposit.transactionType, self.validTransactionType)
        self.assertEqual(deposit.depositMethod, self.validDepositMethod)
        self.assertEqual(deposit.fee, self.validFee)
        self.assertEqual(deposit.origin, self.validOrigin)
        self.assertEqual(deposit.description, self.validDescription)
        self.assertEqual(deposit._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + deposit._timeStamp.isoformat()).encode(), deposit.transactionID))
    # Test constructor with valid values (no fee, origin, or description)
    def test_deposit_constructor_valid_no_fee_origin_description(self):
        deposit = Deposit(self.validUserID, self.validAccountID, self.validAmount, self.validDepositMethod)
        self.assertEqual(deposit.userID, self.validUserID)
        self.assertEqual(deposit.accountID, self.validAccountID)
        self.assertEqual(deposit.amount, self.validAmount)
        self.assertEqual(deposit.transactionType, self.validTransactionType)
        self.assertEqual(deposit.depositMethod, self.validDepositMethod)
        self.assertEqual(deposit.fee, 0.00)
        self.assertIsNone(deposit.origin)
        self.assertIsNone(deposit.description)
        self.assertEqual(deposit._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + deposit._timeStamp.isoformat()).encode(), deposit.transactionID))
   # Test constructuor with invalid (non-string) deposit method
    def test_deposit_constructor_invalid_deposit_method_non_string(self):
        with self.assertRaises(DepositError, msg = "Invalid deposit method"):
            Deposit(self.validUserID, self.validAccountID, self.validAmount, 100.00)
    # Test constructor with invalid (empty string) deposit method
    def test_deposit_constructor_invalid_deposit_method_empty_string(self):
        with self.assertRaises(DepositError, msg = "Invalid deposit method"):
            Deposit(self.validUserID, self.validAccountID, self.validAmount, "")
    # Test constructor with invalid (non-valid) deposit method
    def test_deposit_constructor_invalid_deposit_method_invalid(self):
        with self.assertRaises(DepositError, msg = "Invalid deposit method"):
            Deposit(self.validUserID, self.validAccountID, self.validAmount, "Invalid")

# Test Withdrawal class
class TestWithdrawal(TestTransaction):
    def setUp(self):
        super().setUp()
        self.validWithdrawalMethod = "Cash"
        self.validTransactionType = "Withdrawal"
    # Test Withdrawl Constructor:
    # Test constructor with valid values (all values supplied)
    def test_withdrawl_constructor_valid(self):
        withdrawal = Withdrawal(self.validUserID, self.validAccountID, self.validAmount, self.validWithdrawalMethod, self.validFee, self.validTransactionType, self.validOrigin, self.validDescription)
        self.assertEqual(withdrawal.userID, self.validUserID)
        self.assertEqual(withdrawal.accountID, self.validAccountID)
        self.assertEqual(withdrawal.amount, self.validAmount)
        self.assertEqual(withdrawal.transactionType, self.validTransactionType)
        self.assertEqual(withdrawal.withdrawalMethod, self.validWithdrawalMethod)
        self.assertEqual(withdrawal.fee, self.validFee)
        self.assertEqual(withdrawal.origin, self.validOrigin)
        self.assertEqual(withdrawal.description, self.validDescription)
        self.assertEqual(withdrawal._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + withdrawal._timeStamp.isoformat()).encode(), withdrawal.transactionID))
    # Test constructor with valid values (no fee, origin, or description)
    def test_withdrawl_constructor_valid_no_fee_origin_description(self):
        withdrawal = Withdrawal(self.validUserID, self.validAccountID, self.validAmount, self.validWithdrawalMethod)
        self.assertEqual(withdrawal.userID, self.validUserID)
        self.assertEqual(withdrawal.accountID, self.validAccountID)
        self.assertEqual(withdrawal.amount, self.validAmount)
        self.assertEqual(withdrawal.transactionType, self.validTransactionType)
        self.assertEqual(withdrawal.withdrawalMethod, self.validWithdrawalMethod)
        self.assertEqual(withdrawal.fee, 0.00)
        self.assertIsNone(withdrawal.origin)
        self.assertIsNone(withdrawal.description)
        self.assertEqual(withdrawal._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + withdrawal._timeStamp.isoformat()).encode(), withdrawal.transactionID))
    # Test constructuor with invalid (non-string) withdrawal method
    def test_withdrawal_constructor_invalid_withdrawal_method_non_string(self):
        with self.assertRaises(WithdrawalError, msg = "Invalid withdrawal method"):
            Withdrawal(self.validUserID, self.validAccountID, self.validAmount, 100.00)
    # Test constructor with invalid (empty string) withdrawal method
    def test_withdrawal_constructor_invalid_withdrawal_method_empty_string(self):
        with self.assertRaises(WithdrawalError, msg = "Invalid withdrawal method"):
            Withdrawal(self.validUserID, self.validAccountID, self.validAmount, "")
    # Test constructor with invalid (non-valid) withdrawal method
    def test_withdrawal_constructor_invalid_withdrawal_method_invalid(self):
        with self.assertRaises(WithdrawalError, msg = "Invalid withdrawal method"):
            Withdrawal(self.validUserID, self.validAccountID, self.validAmount, "Invalid")

# Test InternalTransfer class
class TestInternalTransfer(TestTransaction):
    def setUp(self):
        super().setUp()
        self.validTransactionType = "Intra-Transfer"
        self.validDestinationAccountID = "Timm0002"
    
    # Test InternalTransfer Constructor:
    # Test constructor with valid values (all values supplied)
    def test_internal_transfer_constructor_valid(self):
        transfer = InternalTransfer(self.validUserID, self.validAccountID, self.validDestinationAccountID, self.validAmount, self.validTransactionType, self.validFee, self.validOrigin, self.validDescription)
        self.assertEqual(transfer.userID, self.validUserID)
        self.assertEqual(transfer.accountID, self.validAccountID)
        self.assertEqual(transfer.destinationAccountID, self.validDestinationAccountID)
        self.assertEqual(transfer.amount, self.validAmount)
        self.assertEqual(transfer.transactionType, self.validTransactionType)
        self.assertEqual(transfer.fee, self.validFee)
        self.assertEqual(transfer.origin, self.validOrigin)
        self.assertEqual(transfer.description, self.validDescription)
        self.assertEqual(transfer._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + transfer._timeStamp.isoformat()).encode(), transfer.transactionID))
    # Test constructor with valid values (no transaction type, fee, origin, or description)
    def test_internal_transfer_constructor_valid_no_fee_origin_description(self):
        transfer = InternalTransfer(self.validUserID, self.validAccountID, self.validDestinationAccountID, self.validAmount)
        self.assertEqual(transfer.userID, self.validUserID)
        self.assertEqual(transfer.accountID, self.validAccountID)
        self.assertEqual(transfer.destinationAccountID, self.validDestinationAccountID)
        self.assertEqual(transfer.amount, self.validAmount)
        self.assertEqual(transfer.transactionType, self.validTransactionType)
        self.assertEqual(transfer.fee, 0.00)
        self.assertIsNone(transfer.origin)
        self.assertIsNone(transfer.description)
        self.assertEqual(transfer._timeStamp.date(), date.today())
        self.assertTrue(bcrypt.verify((self.validUserID + "-" + self.validTransactionType + "-" + transfer._timeStamp.isoformat()).encode(), transfer.transactionID))
    # Test constructor with invalid (non-string) destination account ID
    def test_internal_transfer_constructor_invalid_destination_accountID_non_string(self):
        with self.assertRaises(TransferError, msg = "Transaction Error: Destination Account ID must be a string"):
            InternalTransfer(self.validUserID, self.validAccountID, 100, self.validAmount)
    # Test constructor with invalid (non-alphanumeric) destination account ID
    def test_internal_transfer_constructor_invalid_destination_accountID_non_alphanumeric(self):
        with self.assertRaises(TransferError, msg = "Transfer Error: Destination Account ID must be alphanumeric"):
            InternalTransfer(self.validUserID, self.validAccountID, "Timm-0002", self.validAmount)
    # Test constructor with invalid (empty string) destination account ID
    def test_internal_transfer_constructor_invalid_destination_accountID_empty_string(self):
        with self.assertRaises(TransferError, msg = "Transaction Error: Destination Account ID cannot be an empty string"):
            InternalTransfer(self.validUserID, self.validAccountID, "", self.validAmount)
    # Test constructor with invalid (same as source) destination account ID
    def test_internal_transfer_constructor_invalid_destination_accountID_same_as_source(self):
        with self.assertRaises(TransferError, msg = "Transaction Error: Destination Account ID cannot be the same as the source account ID"):
            InternalTransfer(self.validUserID, self.validAccountID, self.validAccountID, self.validAmount)


# Test Account class
class TestAccount(TestTransaction):
    def setUp(self):
        super().setUp()
        self.validInitialDeposit = 1000.00
        self.validAccountStatus = "Active"
    # Test Account Constructor:
    # Test constructor with valid values
    def test_account_constructor_valid(self):
        account = Account(self.validAccountID, self.validUserID, self.validInitialDeposit)
        self.assertEqual(account.accountID, self.validAccountID)
        self.assertEqual(account.userID, self.validUserID)
        self.assertEqual(account.balance, self.validInitialDeposit)
        self.assertEqual(account.dateCreated, date.today())
        self.assertEqual(account.status, self.validAccountStatus)
        self.assertEqual(account.transactions, [])
    # Test constructor with invalid (non-string) account ID
    def test_account_constructor_invalid_accountID_non_string(self):
        with self.assertRaises(InvalidAccountIDError, msg = "Account ID Error: Account ID must be a string"):
            Account(100, self.validUserID, self.validInitialDeposit)
    # Test constructor with invalid (non-alphanumeric) account ID
    def test_account_constructor_invalid_accountID_non_alphanumeric(self):
        with self.assertRaises(InvalidAccountIDError, msg = "Account ID Error: Account ID must be alphanumeric"):
            Account("Timm-0001", self.validUserID, self.validInitialDeposit)
    # Test constructor with invalid (empty string) account ID 
    def test_account_constructor_invalid_accountID_empty_string(self):
        with self.assertRaises(InvalidAccountIDError, msg = "Account ID cannot be an empty string"):
            Account("", self.validUserID, self.validInitialDeposit)
    # Test constructor with invalid (non-floating point) initial deposit
    def test_account_constructor_invalid_initial_deposit_non_float(self):
        with self.assertRaises(DepositError, msg = "Initial Deposit Error: Initial Deposit must be a floating point number"):
            Account(self.validAccountID, self.validUserID, "self.validInitialDeposit")
    # Test constructor with invalid (negative) initial deposit
    def test_account_constructor_invalid_initial_deposit_negative(self):
        with self.assertRaises(DepositError, msg = "Initial Deposit Error: Initial Deposit must be greater than or equal to 0"):
            Account(self.validAccountID, self.validUserID, -self.validInitialDeposit)



