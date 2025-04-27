import logging
from datetime import datetime
from typing import List, Optional
from app.accounts.models import Account, Transaction
from app.accounts.repository import AccountRepository, TransactionRepository

class AccountService:
    def __init__(self, account_repository: AccountRepository, transaction_repository: TransactionRepository):
        self.account_repository = account_repository
        self.transaction_repository = transaction_repository

    def get_account_details(self, account_id: str) -> Optional[Account]:
        return self.account_repository.get_by_id(account_id)

    def get_accounts_by_customer(self, customer_id: str) -> List[Account]:
        return self.account_repository.get_by_customer_id(customer_id)

    def calculate_account_balance(self, account_id: str) -> float:
        account = self.get_account_details(account_id)
        if account:
            transactions = self.transaction_repository.get_by_account_id(account_id)
            balance = account.balance
            for transaction in transactions:
                if transaction.status == 'success':
                    if transaction.type in ['deposit', 'transfer_in', 'loan_payment']:
                        balance += transaction.amount
                    elif transaction.type in ['withdrawal', 'transfer_out', 'fees']:
                        balance -= transaction.amount
            return balance
        return 0.0

    def save_account(self, account: Account):
        self.account_repository.update(account)

class TransactionService:
    FRAUD_THRESHOLD = 5000.00
    def __init__(self, transaction_repository: TransactionRepository, account_repository: AccountRepository):
        self.transaction_repository = transaction_repository
        self.account_repository = account_repository

    def get_transactions_by_account(self, account_id: str) -> List[Transaction]:
        return self.transaction_repository.get_by_account_id(account_id)

    def identify_potential_fraud(self, account_id: str) -> List[Transaction]:
        transactions = self.transaction_repository.get_by_account_id(account_id)
        print(len(transactions))
        print('i am here')
        fraudulent = []
        if not transactions:
            return fraudulent

        withdrawal_threshold = 6000
        # suspicious_activity_period = 3600
        # large_withdrawal_count = 3

        recent_large_withdrawals = 0

        for i, transaction in enumerate(transactions):
            if (transaction.status == 'success' and transaction.type == 'withdrawal'
                     and transaction.amount >= withdrawal_threshold ):
                        transaction.fraud_reason = "Unusually high withdrawal amount"
                        fraudulent.append(transaction)
                        recent_large_withdrawals += 1
            elif transaction.status == 'flagged_fraud':
                transaction.fraud_reason = "Transaction is marked as Fraud"
                fraudulent.append(transaction)

        return fraudulent


    def generate_fraud_alert(self, transaction: Transaction):
        return f"Potential fraudulent transaction detected: ID {transaction.transaction_id}, Account {transaction.account_id}, Type {transaction.type}, Amount {transaction.amount}, Timestamp {transaction.timestamp}"

    def process_transactions(self, account_id: str):
        transactions = self.get_transactions_by_account(account_id)
        alerts = []
        for transaction in transactions:
            if transaction.status == 'flagged_fraud':
                alert = self.generate_fraud_alert(transaction)
                alerts.append(alert)
                print(f"Alert: {alert}")
        return alerts

    def process_transfer(self, source_account_id: str, recipient_account_id: str, amount: float) -> Optional[
        Transaction]:
        source_account = self.account_repository.get_by_id(source_account_id)
        recipient_account = self.account_repository.get_by_id(recipient_account_id)

        if not source_account or not recipient_account or amount <= 0 or source_account.balance < amount or source_account_id == recipient_account_id:
            logging.warning(f"Transfer failed: Invalid request from '{source_account_id}' to '{recipient_account_id}' for amount '{amount}'.")
            return None

        timestamp = datetime.now().isoformat()
        transaction_id = self.transaction_repository.generate_unique_id()
        status_out = "completed"
        status_in = "completed"
        if amount > self.FRAUD_THRESHOLD:
            status_out = "flagged_fraud"
            status_in = "flagged_fraud"
            logging.warning(f"Potential fraudulent transfer of '{amount}' from '{source_account_id}' to '{recipient_account_id}' exceeds threshold.")

        # Debit from source
        source_account.balance -= amount
        self.account_repository.update(source_account)
        transaction_out = Transaction(
            transaction_id=transaction_id + "-out",
            account_id=source_account_id,
            type="transfer_out",
            amount=amount,
            timestamp=timestamp,
            status=status_out
        )
        self.transaction_repository.add_transaction(transaction_out)
        logging.info(
            f"Transfer out of '{amount}' from '{source_account_id}' to '{recipient_account_id}' processed with status '{status_out}'. Transaction ID: '{transaction_id}-out'.")

        # Credit to recipient
        recipient_account.balance += amount
        self.account_repository.update(recipient_account)
        transaction_in = Transaction(
            transaction_id=transaction_id + "-in",
            account_id=recipient_account_id,
            type="transfer_in",
            amount=amount,
            timestamp=timestamp,
            status=status_in
        )
        self.transaction_repository.add_transaction(transaction_in)
        logging.info(
            f"Transfer in of '{amount}' to '{recipient_account_id}' from '{source_account_id}' processed with status '{status_in}'. Transaction ID: '{transaction_id}-in'.")

        return transaction_out

    def process_deposit(self, account_id: str, amount: float) -> Optional[Transaction]:
        account = self.account_repository.get_by_id(account_id)
        if not account or amount <= 0:
            logging.warning(f"Deposit failed for account '{account_id}' with amount '{amount}'.")
            return None
        account.balance += amount
        self.account_repository.update(account)
        timestamp = datetime.now().isoformat()
        transaction_id = self.transaction_repository.generate_unique_id()
        transaction = Transaction(
            transaction_id=transaction_id,
            account_id=account_id,
            type="deposit",
            amount=amount,
            timestamp=timestamp,
            status="completed"
        )
        self.transaction_repository.add_transaction(transaction)
        logging.info(f"Deposit of '{amount}' to account '{account_id}' completed. Transaction ID: '{transaction_id}'.")
        return transaction

    def process_withdrawal(self, account_id: str, amount: float) -> Optional[Transaction]:
        account = self.account_repository.get_by_id(account_id)
        if not account or amount <= 0 or account.balance < amount:
            logging.warning(f"Withdrawal failed for account '{account_id}' with amount '{amount}'. Insufficient funds or invalid request.")
            return None

        timestamp = datetime.now().isoformat()
        transaction_id = self.transaction_repository.generate_unique_id()
        status = "completed"
        if amount > self.FRAUD_THRESHOLD:
            status = "flagged_fraud"
            logging.warning(f"Potential fraudulent withdrawal of '{amount}' from account '{account_id}' exceeds threshold.")

        account.balance -= amount
        self.account_repository.update(account)
        transaction = Transaction(
            transaction_id=transaction_id,
            account_id=account_id,
            type="withdrawal",
            amount=amount,
            timestamp=timestamp,
            status=status
        )
        self.transaction_repository.add_transaction(transaction)
        logging.info(f"Withdrawal of '{amount}' from account '{account_id}' processed with status '{status}'. Transaction ID: '{transaction_id}'.")
        return transaction