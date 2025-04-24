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
    def __init__(self, transaction_repository: TransactionRepository):
        self.transaction_repository = transaction_repository

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