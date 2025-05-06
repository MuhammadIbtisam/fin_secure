import tkinter as tk
from tkinter import ttk, messagebox
from app.customers.services import CustomerService
from app.accounts.services import AccountService
from .customer_registration_window import CustomerRegistrationWindow
from presentation.customer_transaction_window import CustomerTransactionWindow

class CustomerLoginWindow(tk.Toplevel):
    def __init__(self, parent, customer_service: CustomerService, account_service: AccountService, on_customer_login):
        super().__init__(parent)
        self.title("Customer Login")
        self.geometry("300x250")
        self.parent = parent
        self.customer_service = customer_service
        self.account_service = account_service
        self.on_customer_login = on_customer_login

        self.customer_id_label = ttk.Label(self, text="Customer Name:")
        self.customer_id_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.customer_id_entry = ttk.Entry(self)
        self.customer_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.login_button = ttk.Button(self, text="Customer Login", command=self.attempt_customer_login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.register_button = ttk.Button(self, text="Register New Customer", command=self.open_registration_window)
        self.register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.grid_columnconfigure(1, weight=1)

    def attempt_customer_login(self):
        customer_name = self.customer_id_entry.get()
        password = self.password_entry.get()
        customer = self.customer_service.authenticate_customer(customer_name, password)
        if customer:
            CustomerTransactionWindow(self, customer.customer_id)
        else:
            messagebox.showerror("Login Failed", "Invalid Customer ID or Password.")

    def open_registration_window(self):
        CustomerRegistrationWindow(self.parent, self.customer_service, self.account_service)
        # self.withdraw()