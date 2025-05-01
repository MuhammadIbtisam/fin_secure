import os
import json
import uuid
from typing import List, Optional
from app.accounts.models import Account, Transaction
from app.utils.data_manager import load_json, save_json, load_csv, save_csv

class AccountRepository:
    def __init__(self, data_file='accounts.json'):
        self.data_file = data_file
        # self.accounts = self._load_accounts()
        self.accounts = self._load_accounts()
        print(f"AccountRepository loaded accounts: {self.accounts}")

    def _load_accounts(self) -> List[Account]:
        print(f"AccountRepository: _load_accounts() called. Attempting to load from: {self.data_file}")
        account_data_list = load_json(self.data_file)
        print(f"AccountRepository: _load_accounts() - Data loaded from JSON: {account_data_list}")
        accounts = []
        # account_data_list = load_json(self.data_file)
        # accounts = []
        for account_data in account_data_list:
            account = Account(
                account_id=account_data.get('account_id'),
                customer_id=account_data.get('customer_id'),
                type=account_data.get('type'),
                balance=account_data.get('balance', 0.0),
                notes=account_data.get('notes', [])
            )
            accounts.append(account)
        return accounts

    def get_all(self) -> List[Account]:
        return self.accounts

    def get_by_id(self, account_id: str) -> Optional[Account]:
        for account in self.accounts:
            if account.account_id == account_id:
                return account
        return None

    def get_by_customer_id(self, customer_id: str) -> List[Account]:
        matching_accounts = [
            account for account in self.accounts if account.customer_id == customer_id
        ]
        return matching_accounts

    def update(self, account_to_update: Account):
        for i, account in enumerate(self.accounts):
            if account.account_id == account_to_update.account_id:
                self.accounts[i] = account_to_update
                self._save_accounts()
                return
        # Handle case where account is not found (optional)

    def _save_accounts(self):
        data_to_save = []
        for account in self.accounts:
            account_data = account.__dict__.copy()
            # Ensure notes are saved as is (they are lists of dictionaries)
            data_to_save.append(account_data)
        save_json(self.data_file, data_to_save)


    def _add_accounts(self, account: Account):
        self.accounts.append(account)
        self._save_accounts()


class TransactionRepository:
    def __init__(self, data_file='transactions.csv'):
        self.data_file = data_file
        self.transactions = self._load_transactions()

    def _load_transactions(self) -> List[Transaction]:
        transaction_data_list = load_csv(self.data_file)
        transactions = []
        for transaction_data in transaction_data_list:
            transaction = Transaction(
                transaction_id=transaction_data.get('transaction_id'),
                account_id=transaction_data.get('account_id'),
                type=transaction_data.get('type'),
                amount=float(transaction_data.get('amount', 0.0)),
                timestamp=transaction_data.get('timestamp'),
                status=transaction_data.get('status')
            )
            transactions.append(transaction)
        return transactions

    def get_all(self) -> List[Transaction]:
        return self.transactions

    def get_by_account_id(self, account_id: str) -> List[Transaction]:
        matching_transactions = [
            transaction for transaction in self.transactions if transaction.account_id == account_id
        ]
        return matching_transactions

    def get_by_status(self, status: str) -> List[Transaction]:
        matching_transactions = [
            transaction for transaction in self.transactions if transaction.status == status
        ]
        return matching_transactions

    def get_by_type(self, type: str) -> List[Transaction]:
        matching_transactions = [
            transaction for transaction in self.transactions if transaction.type == type
        ]
        return matching_transactions

    def generate_unique_id(self):
        return str(uuid.uuid4())

    def add_transaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self._save_transactions()

    def _save_transactions(self):
        data_to_save = []
        for transaction in self.transactions:
            data_to_save.append(transaction.__dict__.copy())

        if data_to_save:
            fieldnames = data_to_save[0].keys()
            save_csv(self.data_file, data_to_save, fieldnames=fieldnames)
        else:
            save_csv(self.data_file, [], fieldnames=[])
