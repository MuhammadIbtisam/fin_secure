import os
import tkinter as tk
from tkinter import ttk, messagebox
from app.auth.user_service import UserService
from app.customers.repository import CustomerRepository
from presentation.customer_login_window import CustomerLoginWindow
from app.customers.services import CustomerService
from app.accounts.services import AccountService
from app.accounts.repository import AccountRepository, TransactionRepository


class LoginWindow(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.title("Login")
        self.geometry("300x190")
        self.parent = parent
        self.on_login_success = on_login_success
        self.user_service = UserService()

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        customers_file_path = os.path.join(data_dir, 'customers.json')
        accounts_file_path = os.path.join(data_dir, 'accounts.json')
        transactions_file_path = os.path.join(data_dir, 'transactions.csv')

        account_repository = AccountRepository(data_file=accounts_file_path)
        transaction_repository = TransactionRepository(data_file=transactions_file_path)
        account_service = AccountService(account_repository, transaction_repository)
        customer_repository = CustomerRepository(data_file=customers_file_path)
        self.customer_service = CustomerService(customer_repository, account_service)
        self.account_service = account_service

        self.username_label = ttk.Label(self, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.login_button = ttk.Button(self, text="Login", command=self.attempt_login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.login_as_customer_button = ttk.Button(self, text="Customer Window", command=self.login_as_customer)
        self.login_as_customer_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.grid_columnconfigure(1, weight=1)

    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        role = self.user_service.authenticate_user(username, password)
        if role:
            self.on_login_success(role)  # Pass the role back
            self.destroy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def login_as_customer(self):
        CustomerLoginWindow(self.parent, self.customer_service, self.account_service, self.on_login_success)
        self.withdraw()