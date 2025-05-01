import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.customers.models import Interaction
from presentation.customer_transaction_window import CustomerTransactionWindow


class CustomersManagementWindow(tk.Toplevel):
    def __init__(self, parent, customer_service):
        super().__init__(parent)
        self.title("Customer Management")
        self.geometry("1400x900")
        self.parent_app = parent  # To access the main app and its attributes
        self.customer_service = customer_service
        self.current_customer = None
        self.feedback_label = ttk.Label(self, text="", foreground="green")
        self.feedback_label.pack(pady=5)
        self.logged_in_role = self.parent_app.logged_in_role
        self.create_widgets()
        self.apply_permissions()
        self.load_customers() # Load customers on initialization

    def create_widgets(self):
        # Search Frame
        search_frame = ttk.LabelFrame(self, text="Search Customer")
        search_frame.pack(padx=10, pady=5, fill="x")
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)
        search_button = ttk.Button(search_frame, text="Search", command=self.search_customer)
        search_button.pack(side="left", padx=5)
        self.search_button = search_button

        # add_new_button = ttk.Button(search_frame, text="Add New Customer", command=self.add_new_customer)
        # add_new_button.pack(side="right", padx=5)
        # self.add_new_button = add_new_button

        # Customer List Frame
        list_frame = ttk.LabelFrame(self, text="Customer List")
        list_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.customer_list = tk.Listbox(list_frame)
        self.customer_list.pack(fill="both", expand=True)
        self.customer_list.bind('<<ListboxSelect>>', self.load_customer_details)

        # Details Frame
        self.details_frame = ttk.LabelFrame(self, text="Customer Details") # Make self.details_frame an instance attribute
        self.details_frame.pack(padx=10, pady=10, fill="x")
        self.name_label = ttk.Label(self.details_frame, text="Name:")
        self.name_label.pack(pady=2, anchor="w")
        self.id_label = ttk.Label(self.details_frame, text="ID:")
        self.id_label.pack(pady=2, anchor="w")
        self.email_label = ttk.Label(self.details_frame, text="Email:")
        self.email_label.pack(pady=2, anchor="w")
        self.phone_label = ttk.Label(self.details_frame, text="Phone:")
        self.phone_label.pack(pady=2, anchor="w")
        self.accounts_label = ttk.Label(self.details_frame, text="Accounts:")
        self.accounts_label.pack(pady=2, anchor="w")
        self.last_interaction_label = ttk.Label(self.details_frame, text="Last Interaction:")
        self.last_interaction_label.pack(pady=2, anchor="w")
        self.total_interactions_label = ttk.Label(self.details_frame, text="Total Interactions:")
        self.total_interactions_label.pack(pady=2, anchor="w")


        delete_button = ttk.Button(self.details_frame, text="Delete Customer",
                                   command=self.delete_customer)
        delete_button.pack(pady=5)
        self.delete_button = delete_button

        self.view_transactions_button = ttk.Button(self.details_frame, text="View Transactions",
                                                   command=self.open_customer_transactions)
        self.view_transactions_button.pack(pady=5, fill="x")

        # Interaction Log Frame
        log_frame = ttk.LabelFrame(self, text="Interaction Log")
        log_frame.pack(padx=10, pady=5, fill="both", expand=True)
        self.log_text = tk.Text(log_frame, height=10, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar = ttk.Scrollbar(log_frame, command=self.log_text.yview)
        log_scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=log_scrollbar.set)

        # New Note Section
        add_note_frame = ttk.LabelFrame(self, text="Add New Note")
        add_note_frame.pack(padx=10, pady=5, fill="x")
        ttk.Label(add_note_frame, text="Note:").pack(anchor="w")
        self.new_note_text = tk.Text(add_note_frame, height=3)
        self.new_note_text.pack(fill="x")
        add_button = ttk.Button(add_note_frame, text="Add Note", command=self.add_interaction)
        add_button.pack(pady=5)
        self.add_note_button = add_button

    def add_new_customer(self):
        add_dialog = tk.Toplevel(self)
        add_dialog.title("Add New Customer")

        ttk.Label(add_dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        name_entry = ttk.Entry(add_dialog)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_dialog, text="ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        id_entry = ttk.Entry(add_dialog)
        id_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_dialog, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        email_entry = ttk.Entry(add_dialog)
        email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(add_dialog, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        phone_entry = ttk.Entry(add_dialog)
        phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        def save_new_customer():
            name = name_entry.get()
            customer_id = id_entry.get()
            email = email_entry.get()
            phone = phone_entry.get()

            if not all([name, customer_id, email, phone]):
                messagebox.showerror("Error", "All fields are required.")
                return

            new_customer_data = {
                "customer_id": customer_id,
                "name": name,
                "contact_info": {
                    "email": email,
                    "phone": phone
                },
                "account_ids": [],
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

            try:
                self.customer_service.add_customer(new_customer_data)
                messagebox.showinfo("Success", f"Customer '{name}' (ID: {customer_id}) added successfully.")
                self.load_customers()
                add_dialog.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Error adding customer: {e}")

        save_button = ttk.Button(add_dialog, text="Save", command=save_new_customer)
        save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        add_dialog.grid_columnconfigure(1, weight=1)


    def delete_customer(self):
        selected_index = self.customer_list.curselection()
        if not selected_index:
            messagebox.showinfo("Info", "Please select a customer to delete.")
            return

        selected_customer_id = self.get_customer_id_from_list(selected_index[0])
        if not selected_customer_id:
            messagebox.showerror("Error", "Could not retrieve customer ID for deletion.")
            return

        customer_name = self.get_customer_name_from_list(selected_index[0])

        if messagebox.askyesno("Confirm Delete",
                               f"Are you sure you want to delete customer '{customer_name}' (ID: {selected_customer_id})?"):
            try:
                self.customer_service.delete_customer(selected_customer_id)
                messagebox.showinfo("Success",
                                    f"Customer '{customer_name}' (ID: {selected_customer_id}) deleted successfully.")
                self.load_customers()
                self.clear_customer_details()
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting customer: {e}")


    def get_customer_id_from_list(self, index):
        customer_text = self.customer_list.get(index)
        start_index = customer_text.find('(ID: ') + 5
        end_index = customer_text.find(')')
        if start_index != -1 and end_index != -1:
            return customer_text[start_index:end_index].strip()
        return None

    def get_customer_name_from_list(self, index):
        customer_text = self.customer_list.get(index)
        end_index = customer_text.find('(')
        if end_index != -1:
            return customer_text[:end_index].strip()
        return "Unknown Customer"

    def clear_customer_details(self):
        self.name_label.config(text="Name:")
        self.id_label.config(text="ID:")
        self.email_label.config(text="Email:")
        self.phone_label.config(text="Phone:")
        self.accounts_label.config(text="Accounts:")
        self.last_interaction_label.config(text="Last Interaction:")
        self.total_interactions_label.config(text="Total Interactions:")
        if hasattr(self, 'log_text'): # Check if log_text exists before trying to configure it
            self.log_text.config(state="normal")
            self.log_text.delete("1.0", tk.END)
            self.log_text.config(state="disabled")

    def apply_permissions(self):
        if self.logged_in_role == "Customer Service Agent":
            if hasattr(self, 'search_button'):
                self.search_button.config(state="normal")
            if hasattr(self, 'add_note_button'):
                self.add_note_button.config(state="normal")
            if hasattr(self, 'delete_button'):
                self.delete_button.config(state="disabled")
            if hasattr(self, 'add_new_button'):
                self.add_new_button.config(state="disabled")
        elif self.logged_in_role == "Senior Customer Service Agent":
            if hasattr(self, 'search_button'):
                self.search_button.config(state="normal")
            if hasattr(self, 'add_note_button'):
                self.add_note_button.config(state="normal")
            if hasattr(self, 'delete_button'):
                self.delete_button.config(state="disabled")
            if hasattr(self, 'add_new_button'):
                self.add_new_button.config(state="normal")
        elif self.logged_in_role == "Administrator":
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.config(state="normal")
                elif isinstance(widget, ttk.Entry):
                    widget.config(state="normal")
                elif isinstance(widget, tk.Text):
                    widget.config(state="normal")
        elif self.logged_in_role == "Fraud Analyst":
            messagebox.showerror("Access Denied", "Your role does not have permission to access Customer Management.")
            self.destroy()
        else:
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.config(state="disabled")
                elif isinstance(widget, ttk.Entry):
                    widget.config(state="disabled")
                elif isinstance(widget, tk.Text):
                    widget.config(state="disabled")
            messagebox.showerror("Access Denied", "Your role does not have sufficient permissions.")
            self.destroy()

    def search_customer(self):
        search_term = self.search_entry.get()
        customer = self.customer_service.get_customer_profile(search_term)

        if customer:
            self.customer_list.delete(0, tk.END)
            self.customer_list.insert(tk.END, f"{customer.name} (ID: {customer.customer_id})")
            self.current_customer = customer
            self.load_customer_details(None)
        else:
            self.customer_list.delete(0, tk.END)
            self.clear_customer_details()
            self.feedback_label.config(text="Customer not found.", foreground="red")
            self.after(3000, lambda: self.feedback_label.config(text="", foreground="green"))

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

            self.update_interaction_log_display()
        else:
            self.clear_customer_details()

    def add_interaction(self):
        if self.current_customer and self.logged_in_role in ["Customer Service Agent", "Administrator"]:
            note = self.new_note_text.get("1.0", tk.END).strip()
            if note:
                now = datetime.now()
                new_interaction = Interaction(
                    date=now.strftime("%Y-%m-%d %H:%M:%S"),
                    type="Note",
                    notes=note
                )
                self.current_customer.interaction_log.append(new_interaction)
                self.update_interaction_log_display()
                try:
                    self.customer_service.save_customer_profile(self.current_customer)
                    self.new_note_text.delete("1.0", tk.END)
                    self.feedback_label.config(text="Note added successfully.", foreground="green")
                    self.after(3000, lambda: self.feedback_label.config(text="", foreground="green"))
                except Exception as e:
                    self.feedback_label.config(text=f"Error saving note: {e}", foreground="red")
            else:
                self.feedback_label.config(text="Please enter a note.", foreground="red")
                self.after(3000, lambda: self.feedback_label.config(text="", foreground="green"))
        elif not self.current_customer:
            self.feedback_label.config(text="No customer selected.", foreground="red")
            self.after(3000, lambda: self.feedback_label.config(text="", foreground="green"))
        else:
            messagebox.showerror("Permission Denied", "Your role is not allowed to add notes.")

    def update_interaction_log_display(self):
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        for interaction in self.current_customer.interaction_log:
            self.log_text.insert(tk.END,
                                 f"Date: {interaction.date}, Type: {interaction.type}, Notes: {interaction.notes}\n")
        self.log_text.config(state="disabled")

    def load_customers(self):
        self.customer_list.delete(0, tk.END)  # Clear the current list
        customers = self.customer_service.get_all_customers()
        for customer in customers:
            self.customer_list.insert(tk.END, f"{customer.name} (ID: {customer.customer_id})")

    def open_customer_transactions(self):
        selected_index = self.customer_list.curselection()
        if selected_index:
            customer_text = self.customer_list.get(selected_index[0])
            customer_id = self.get_customer_id_from_list(selected_index[0])
            if customer_id:
                customer_transaction_window = CustomerTransactionWindow(self, customer_id)
        else:
            messagebox.showinfo("Info", "Please select a customer to view transactions.")