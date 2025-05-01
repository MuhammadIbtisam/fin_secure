from typing import Optional
from datetime import datetime
from typing import List

class Account:
    def __init__(self, account_id: str, customer_id: str, type: str, balance: float = 0.0, notes: str = None):
        self.account_id = account_id
        self.customer_id = customer_id
        self.type = type
        self.balance = balance
        self.notes = notes if notes is not None else []

class Transaction:
    def __init__(self, transaction_id: str, account_id: str, type: str, amount: float, timestamp: str, status: str):
        self.transaction_id = transaction_id
        self.account_id = account_id
        self.type = type
        self.amount = amount
        self.timestamp = timestamp
        self.status = status