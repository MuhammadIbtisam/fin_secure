import tkinter as tk
from tkinter import ttk, messagebox

from app.accounts.models import Account
from app.customers.services import CustomerService
from app.customers.models import Customer, ContactInfo
from app.accounts.services import AccountService
import uuid

class CustomerRegistrationWindow(tk.Toplevel):
    def __init__(self, parent, customer_service: CustomerService, account_service: AccountService):
        super().__init__(parent)
        self.title("Customer Registration")
        self.geometry("400x250")
        self.parent = parent
        self.customer_service = customer_service
        self.account_service = account_service

        self.name_label = ttk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.name_entry = ttk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        self.password_label = ttk.Label(self, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        self.email_label = ttk.Label(self, text="Email:")
        self.email_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.phone_label = ttk.Label(self, text="Phone:")
        self.phone_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.register_button = ttk.Button(self, text="Register", command=self.register_new_customer)
        self.register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

        self.grid_columnconfigure(1, weight=1)

    def register_new_customer(self):
        name = self.name_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        if not name or not password or not email:
            messagebox.showerror("Registration Error", "Please fill in all required fields.")
            return

        if self.customer_service.is_name_unique(name):
            customer_id = str(uuid.uuid4())[:4]
            account_id = str(uuid.uuid4())[:8]
            new_customer = {
                "customer_id": customer_id,
                "name": name,
                "password": password,
                "contact_info": {
                    "email": email,
                    "phone": phone
                },
                "account_ids": [account_id],
                "account_summary": {},
                "products": [],
                "interaction_log": [],
                "last_interaction_date": None,
                "total_interactions": 0,
                "advice_history": [],
                "personalized_advice": [],
                "date_of_birth": None,
                "address": None,
                "customer_segment": None,
                "consent": None
            }

            create_account = Account(account_id = account_id, customer_id = customer_id,
                                     type="Customer", balance= 0, notes= "default account")


            # new_customer = Customer(
            #     customer_id=customer_id,
            #     name=name,
            #     password=password,
            #     contact_info=contact_info,
            #     account_ids=[],
            #     account_summary={},
            #     products=[],
            #     interaction_log=[],
            #     last_interaction_date=None,
            #     total_interactions=0,
            #     advice_history=[],
            #     personalized_advice=[],
            #     date_of_birth=None,
            #     address=None,
            #     customer_segment=None,
            #     consent=None
            # )
            try:
                self.customer_service.add_customer(new_customer)
                self.account_service.add_account(create_account)
                self.destroy()
                messagebox.showinfo("Registration Successful", f"Registration successful! Your Customer ID is: {customer_id}")
                # self.parent.deiconify() # Show the main login window again
            except Exception as e:
                messagebox.showerror("Error", f"Error adding customer: {e}")
        else:
            messagebox.showerror("Registration Error", f"The name '{name}' is already taken. Please choose a different name.")