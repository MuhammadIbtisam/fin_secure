
import tkinter as tk
from tkinter import ttk

class CustomersManagementWindow(tk.Toplevel):
    def __init__(self, parent, customer_service):
        super().__init__(parent)
        self.title("Customer Management")
        self.geometry("800x600")
        self.customer_service = customer_service
        self.current_customer = None

        # Search Frame
        search_frame = ttk.LabelFrame(self, text="Search Customer")
        search_frame.pack(padx=10, pady=10, fill="x")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_customer)
        search_button.pack(side="left", padx=5)

        # Customer List Frame
        list_frame = ttk.LabelFrame(self, text="Customer List")
        list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.customer_list = tk.Listbox(list_frame)
        self.customer_list.pack(fill="both", expand=True)
        self.customer_list.bind('<<ListboxSelect>>', self.load_customer_details)

        # Details Frame
        details_frame = ttk.LabelFrame(self, text="Customer Details")
        details_frame.pack(padx=10, pady=10, fill="x")
        self.name_label = ttk.Label(details_frame, text="Name:")
        self.name_label.pack(pady=5, anchor="w")
        self.id_label = ttk.Label(details_frame, text="ID:")
        self.id_label.pack(pady=5, anchor="w")


    def search_customer(self):
        search_term = self.search_entry.get()

        # customer = self.customer_service.get_customer_profile(search_term)
        customer = self.customer_service.get_customer_profile(search_term)
        print(f"Customer Name: {customer.name}")
        print('I am here 2')

        if customer:
            self.customer_list.delete(0, tk.END)
            self.customer_list.insert(tk.END, f"{customer.name} (ID: {customer.customer_id})")
            self.current_customer = customer
            self.load_customer_details(None)
        else:
            self.customer_list.delete(0, tk.END)
            self.name_label.config(text="Name:")
            self.id_label.config(text="ID:")

            ttk.Label(self, text="Customer not found.", foreground="red").pack()

    def load_customer_details(self, event):
        if self.current_customer:
            self.name_label.config(text=f"Name: {self.current_customer.name}")
            self.id_label.config(text=f"ID: {self.current_customer.customer_id}")
