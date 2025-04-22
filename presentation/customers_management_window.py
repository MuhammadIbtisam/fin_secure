
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
        self.name_label.pack(pady=2, anchor="w")
        self.id_label = ttk.Label(details_frame, text="ID:")
        self.id_label.pack(pady=2, anchor="w")
        self.email_label = ttk.Label(details_frame, text="Email:")
        self.email_label.pack(pady=2, anchor="w")
        self.phone_label = ttk.Label(details_frame, text="Phone:")
        self.phone_label.pack(pady=2, anchor="w")
        self.accounts_label = ttk.Label(details_frame, text="Accounts:")
        self.accounts_label.pack(pady=2, anchor="w")
        self.last_interaction_label = ttk.Label(details_frame, text="Last Interaction:")
        self.last_interaction_label.pack(pady=2, anchor="w")
        self.total_interactions_label = ttk.Label(details_frame, text="Total Interactions:")
        self.total_interactions_label.pack(pady=2, anchor="w")

        # Interaction Log Frame
        log_frame = ttk.LabelFrame(self, text="Interaction Log")
        log_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.log_text = tk.Text(log_frame, height=10, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=log_scrollbar.set)


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
            self.email_label.config(text="Email:")
            self.phone_label.config(text="Phone:")
            self.accounts_label.config(text="Accounts:")
            self.last_interaction_label.config(text="Last Interaction:")
            self.total_interactions_label.config(text="Total Interactions:")
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", tk.END)
            self.log_text.config(state="disabled")
            ttk.Label(self, text="Customer not found.", foreground="red").pack()

    def load_customer_details(self, event):
        if self.current_customer:
            self.name_label.config(text=f"Name: {self.current_customer.name}")
            self.id_label.config(text=f"ID: {self.current_customer.customer_id}")
            self.email_label.config(text=f"Email: {self.current_customer.contact_info.email}")
            self.phone_label.config(text=f"Phone: {self.current_customer.contact_info.phone}")
            self.accounts_label.config(text=f"Accounts: {', '.join(self.current_customer.account_ids)}")
            self.last_interaction_label.config(
                text=f"Last Interaction: {self.current_customer.last_interaction_date or 'N/A'}")
            self.total_interactions_label.config(text=f"Total Interactions: {self.current_customer.total_interactions}")

            self.log_text.config(state="normal")
            self.log_text.delete("1.0", tk.END)
            for interaction in self.current_customer.interaction_log:
                self.log_text.insert(tk.END,
                                     f"Date: {interaction.date}, Type: {interaction.type}, Notes: {interaction.notes}\n")
            self.log_text.config(state="disabled")