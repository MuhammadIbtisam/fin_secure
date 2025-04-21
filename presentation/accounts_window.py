
import tkinter as tk
from tkinter import ttk

class AccountsWindow(tk.Toplevel):
    def __init__(self, parent, account_service, transaction_service):
        super().__init__(parent)
        self.title("Accounts")
        self.geometry("800x600")
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.current_account = None

        # Account Search Frame
        account_search_frame = ttk.LabelFrame(self, text="Search Accounts")
        account_search_frame.pack(padx=10, pady=10, fill="x")
        self.account_search_entry = ttk.Entry(account_search_frame)
        self.account_search_entry.pack(side="left", padx=5, fill="x", expand=True)
        account_search_button = ttk.Button(account_search_frame, text="Search", command=self.search_accounts)
        account_search_button.pack(side="left", padx=5)

        # Account List Frame
        account_list_frame = ttk.LabelFrame(self, text="Account List")
        account_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.account_list = ttk.Treeview(account_list_frame, columns=("ID", "Type", "Balance"), show="headings")
        self.account_list.heading("ID", text="Account ID")
        self.account_list.heading("Type", text="Type")
        self.account_list.heading("Balance", text="Balance")
        self.account_list.pack(fill="both", expand=True)
        self.account_list.bind('<<TreeviewSelect>>', self.load_transactions)

        # Transaction List Frame
        transaction_list_frame = ttk.LabelFrame(self, text="Transactions")
        transaction_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.transaction_list = ttk.Treeview(transaction_list_frame, columns=("ID", "Type", "Amount", "Timestamp", "Status"), show="headings")
        self.transaction_list.heading("ID", text="Transaction ID")
        self.transaction_list.heading("Type", text="Type")
        self.transaction_list.heading("Amount", text="Amount")
        self.transaction_list.heading("Timestamp", text="Timestamp")
        self.transaction_list.heading("Status", text="Status")
        self.transaction_list.pack(fill="both", expand=True)

    def search_accounts(self):
        search_term = self.account_search_entry.get()

        account = self.account_service.get_account_details(search_term)
        if account:
            for item in self.account_list.get_children():
                self.account_list.delete(item)
            self.account_list.insert("", tk.END, values=(account.account_id, account.type, account.balance))
            self.current_account = account
            self.load_transactions(None)
        else:
            pass

    def load_transactions(self, event):
        if self.current_account:
            transactions = self.transaction_service.get_transactions_by_account(self.current_account.account_id)
            for item in self.transaction_list.get_children():
                self.transaction_list.delete(item)
            for transaction in transactions:
                self.transaction_list.insert("", tk.END, values=(transaction.transaction_id, transaction.type, transaction.amount, transaction.timestamp, transaction.status))