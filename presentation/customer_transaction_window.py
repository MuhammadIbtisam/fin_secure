import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.accounts.repository import AccountRepository, TransactionRepository
from app.accounts.services import AccountService as AccService, TransactionService as TransService


class CustomerTransactionWindow(tk.Toplevel):
    def __init__(self, parent, customer_id):
        super().__init__(parent)
        print(f"CustomerTransactionWindow initialized with customer ID: {customer_id}")
        self.title("Your Transactions")
        self.customer_id = customer_id

        # Determine the path to the data directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, '..', 'data')  # Assuming 'data' is one level up from 'presentation'

        accounts_file_path = os.path.join(data_dir, 'accounts.json')
        transactions_file_path = os.path.join(data_dir, 'transactions.csv')

        print(f"Attempting to load accounts from: {accounts_file_path}")
        print(f"Attempting to load transactions from: {transactions_file_path}")

        self.account_repository = AccountRepository(data_file=accounts_file_path)
        self.transaction_repository = TransactionRepository(data_file=transactions_file_path)
        self.account_service = AccService(self.account_repository, self.transaction_repository)
        self.transaction_service = TransService(self.transaction_repository, self.account_repository)

        self.selected_account_id = tk.StringVar(self)
        self.transaction_type = tk.StringVar(self)

        self.create_widgets()
        self.load_customer_accounts()

        self.show_transaction_details_area()
        self.account_balances = {}

    def create_widgets(self):
        ttk.Label(self, text="Select Account:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.account_combobox = ttk.Combobox(self, textvariable=self.selected_account_id)
        self.account_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.account_combobox.bind("<<ComboboxSelected>>", lambda event: self.show_transaction_details_area())

        ttk.Label(self, text="Current Balance:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.balance_label = ttk.Label(self, text="")
        self.balance_label.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Transaction Type Selection
        ttk.Label(self, text="Choose Transaction Type:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.transaction_type_combobox = ttk.Combobox(self, textvariable=self.transaction_type,
                                                      values=["Deposit", "Withdrawal", "Transfer",
                                                              "View History"])
        self.transaction_type_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.transaction_type_combobox.bind("<<ComboboxSelected>>", lambda event: self.show_transaction_details_area())

        # Transaction Details Area (will be dynamically updated)
        self.details_frame = ttk.LabelFrame(self, text="Transaction Details")
        self.details_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Status/Feedback Area
        self.status_label = ttk.Label(self, text="")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        # Navigation (for now, just a close button)
        close_button = ttk.Button(self, text="Close", command=self.destroy)
        close_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10)

        self.grid_columnconfigure(1, weight=1)


    def load_customer_accounts(self):
        print(f"Fetching accounts for customer ID: {self.customer_id}")
        accounts = self.account_service.get_accounts_by_customer(self.customer_id)
        print(f"Accounts fetched: {accounts}")
        account_ids = [account.account_id for account in accounts]
        print(f"Account IDs to populate combobox: {account_ids}")
        self.account_combobox['values'] = account_ids
        self.account_balances = {account.account_id: account.balance for account in accounts}
        if account_ids:
            self.selected_account_id.set(account_ids[0])
            self.update_balance_display(None)
            self.show_transaction_details_area()
        else:
            self.balance_label.config(text="No accounts available for this customer.")

    def update_balance_display(self, event):
        selected_account = self.selected_account_id.get()
        if selected_account in self.account_balances:
            self.balance_label.config(text=f"£{self.account_balances[selected_account]:.2f}")  # Format as currency

    def show_transaction_details_area(self):
        # Clear previous details
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_type = self.transaction_type.get()
        selected_account = self.selected_account_id.get()

        if not selected_account:
            ttk.Label(self.details_frame, text="Please select an account.").pack(padx=5, pady=5, anchor="w")
            return

        vcmd = (self.register(self._validate_positive_float), '%P')
        invalid_cmd = (self.register(lambda: self.bell()),)  # Optional: Make a beep sound on invalid input

        if selected_type == "Deposit":
            ttk.Label(self.details_frame, text="Amount:").pack(padx=5, pady=5, anchor="w")
            self.deposit_amount_entry = ttk.Entry(self.details_frame, validate="focusout", validatecommand=vcmd,
                                                  invalidcommand=invalid_cmd)
            self.deposit_amount_entry.pack(padx=5, pady=5, fill="x")
            deposit_button = ttk.Button(self.details_frame, text="Deposit", command=self.handle_deposit)
            deposit_button.pack(padx=5, pady=10)
        elif selected_type == "Withdrawal":
            ttk.Label(self.details_frame, text="Amount:").pack(padx=5, pady=5, anchor="w")
            self.withdraw_amount_entry = ttk.Entry(self.details_frame, validate="focusout", validatecommand=vcmd,
                                                   invalidcommand=invalid_cmd)
            self.withdraw_amount_entry.pack(padx=5, pady=5, fill="x")
            withdraw_button = ttk.Button(self.details_frame, text="Withdraw", command=self.handle_withdrawal)
            withdraw_button.pack(padx=5, pady=10)
        elif selected_type == "Transfer":
            ttk.Label(self.details_frame, text="Recipient Account ID:").pack(padx=5, pady=5, anchor="w")
            self.transfer_recipient_entry = ttk.Entry(self.details_frame)
            self.transfer_recipient_entry.pack(padx=5, pady=5, fill="x")
            ttk.Label(self.details_frame, text="Amount:").pack(padx=5, pady=5, anchor="w")
            self.transfer_amount_entry = ttk.Entry(self.details_frame, validate="focusout", validatecommand=vcmd,
                                                  invalidcommand=invalid_cmd)
            self.transfer_amount_entry.pack(padx=5, pady=5, fill="x")
            transfer_button = ttk.Button(self.details_frame, text="Transfer", command=self.handle_transfer)
            transfer_button.pack(padx=5, pady=10)
        elif selected_type == "View History":
            self.create_transaction_history_view()

    def _validate_positive_float(self, new_value):
        if not new_value:
            return True
        try:
            value = float(new_value)
            return value > 0
        except ValueError:
            return False

    def create_transaction_history_view(self):
        selected_account = self.selected_account_id.get()
        if not selected_account:
            ttk.Label(self.details_frame, text="Please select an account to view history.").pack(padx=5, pady=5, anchor="w")
            return

        transactions = self.transaction_service.get_transactions_by_account(selected_account)

        tree = ttk.Treeview(self.details_frame, columns=("ID", "Type", "Amount", "Timestamp", "Status"))
        tree.heading("#1", text="ID")
        tree.heading("#2", text="Type")
        tree.heading("#3", text="Amount")
        tree.heading("#4", text="Timestamp")
        tree.heading("#5", text="Status")
        tree.pack(padx=5, pady=5, fill="both", expand=True)

        for trans in transactions:
            formatted_amount = f"£{trans.amount:.2f}"
            tree.insert("", tk.END, values=(trans.transaction_id, trans.type, formatted_amount, trans.timestamp, trans.status))

    def handle_deposit(self):
        amount_str = self.deposit_amount_entry.get()
        selected_account = self.selected_account_id.get()
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.status_label.config(text="Please enter a positive deposit amount.")
                return
            transaction = self.transaction_service.process_deposit(selected_account, amount)
            if transaction:
                self.status_label.config(
                    text=f"Deposit of £{amount:.2f} to account '{selected_account}' successful. Transaction ID: {transaction.transaction_id}")
                self.load_customer_accounts()
                self.show_transaction_details_area()
            else:
                self.status_label.config(text="Deposit failed. Please check logs for details.")
        except ValueError:
            self.status_label.config(text="Invalid amount format. Please enter a number.")

    def handle_withdrawal(self):
        amount_str = self.withdraw_amount_entry.get()
        selected_account = self.selected_account_id.get()
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.status_label.config(text="Please enter a positive withdrawal amount.")
                return
            if messagebox.askokcancel("Confirm Withdrawal",
                                      f"Confirm withdrawal of £{amount:.2f} from account '{selected_account}'?"):
                transaction = self.transaction_service.process_withdrawal(selected_account, amount)
                if transaction:
                    if transaction.status == "flagged_fraud":
                        self.status_label.config(
                            text=f"Withdrawal of £{amount:.2f} from account '{selected_account}' processed. This transaction has been flagged as potential fraud for review.")
                    else:
                        self.status_label.config(
                            text=f"Withdrawal of £{amount:.2f} from account '{selected_account}' successful. Transaction ID: {transaction.transaction_id}")
                    self.load_customer_accounts()
                    self.show_transaction_details_area()
                else:
                    self.status_label.config(text="Withdrawal failed. Insufficient funds or account issue.")
        except ValueError:
            self.status_label.config(text="Invalid amount format. Please enter a number.")

    def handle_transfer(self):
        recipient_account_id = self.transfer_recipient_entry.get()
        amount_str = self.transfer_amount_entry.get()
        selected_account = self.selected_account_id.get()
        try:
            amount = float(amount_str)
            if amount <= 0:
                self.status_label.config(text="Please enter a positive transfer amount.")
                return
            if selected_account == recipient_account_id:
                self.status_label.config(text="Cannot transfer funds to the same account.")
                return
            if messagebox.askokcancel("Confirm Transfer",
                                      f"Confirm transfer of £{amount:.2f} from account '{selected_account}' to '{recipient_account_id}'?"):
                transaction = self.transaction_service.process_transfer(selected_account, recipient_account_id, amount)
                if transaction:
                    if transaction.status == "flagged_fraud":
                        self.status_label.config(
                            text=f"Transfer of £{amount:.2f} from account '{selected_account}' to '{recipient_account_id}' processed. This transaction has been flagged as potential fraud for review.")
                    else:
                        self.status_label.config(
                            text=f"Transfer of £{amount:.2f} from account '{selected_account}' to '{recipient_account_id}' successful. Transaction ID: {transaction.transaction_id}")
                    self.load_customer_accounts()
                    self.show_transaction_details_area()
                else:
                    self.status_label.config(text="Transfer failed. Invalid recipient account or insufficient funds.")
        except ValueError:
            self.status_label.config(text="Invalid amount format. Please enter a number.")