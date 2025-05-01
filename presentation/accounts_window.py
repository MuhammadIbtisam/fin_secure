import tkinter as tk
from datetime import datetime
from tkinter import ttk, messagebox

class AccountsWindow(tk.Toplevel):
    def __init__(self, parent, account_service, transaction_service):
        super().__init__(parent)
        self.title("Accounts")
        self.geometry("1500x800")
        self.parent_app = parent
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.current_account = None
        self.logged_in_role = self.parent_app.logged_in_role
        self.create_widgets()
        self.apply_permissions()

    def create_widgets(self):
        # Account Search Frame
        account_search_frame = ttk.LabelFrame(self, text="Search Accounts")
        account_search_frame.pack(padx=10, pady=10, fill="x")
        self.account_search_entry = ttk.Entry(account_search_frame)
        self.account_search_entry.pack(side="left", padx=5, fill="x", expand=True)
        search_button = ttk.Button(account_search_frame, text="Search", command=self.search_accounts)
        search_button.pack(side="left", padx=5)
        self.search_button = search_button

        # Account List Frame (using Treeview)
        account_list_frame = ttk.LabelFrame(self, text="Account List")
        account_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.account_list = ttk.Treeview(account_list_frame, columns=("ID", "Type", "Balance"), show="headings")
        self.account_list.heading("ID", text="Account ID")
        self.account_list.heading("Type", text="Type")
        self.account_list.heading("Balance", text="Balance")
        self.account_list.pack(fill="both", expand=True)
        self.account_list.bind('<<TreeviewSelect>>', self.load_transactions)

        # Account Details Frame
        account_details_frame = ttk.LabelFrame(self, text="Account Details")
        account_details_frame.pack(padx=10, pady=10, fill="x")
        self.account_type_label = ttk.Label(account_details_frame, text="Type:")
        self.account_type_label.pack(pady=2, anchor="w")
        self.account_balance_label = ttk.Label(account_details_frame, text="Balance:")
        self.account_balance_label.pack(pady=2, anchor="w")

        # Transaction List Frame
        transaction_list_frame = ttk.LabelFrame(self, text="Transactions")
        transaction_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.transaction_list = ttk.Treeview(transaction_list_frame,
                                             columns=("ID", "Type", "Amount", "Timestamp", "Status"), show="headings")
        self.transaction_list.heading("ID", text="Transaction ID")
        self.transaction_list.heading("Type", text="Type")
        self.transaction_list.heading("Amount", text="Amount")
        self.transaction_list.heading("Timestamp", text="Timestamp")
        self.transaction_list.heading("Status", text="Status")
        self.transaction_list.pack(fill="both", expand=True)

        # Notes Section
        notes_frame = ttk.LabelFrame(self, text="Account Notes")
        notes_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.notes_text = tk.Text(notes_frame, height=5, state="disabled")
        self.notes_text.pack(side="left", fill="both", expand=True)
        notes_scrollbar = ttk.Scrollbar(notes_frame, command=self.notes_text.yview)
        notes_scrollbar.pack(side="right", fill="y")
        self.notes_text.config(yscrollcommand=notes_scrollbar.set)

        add_note_frame = ttk.LabelFrame(self, text="Add New Note")
        add_note_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(add_note_frame, text="Note:").pack(anchor="w")
        self.new_note_text = tk.Text(add_note_frame, height=2)
        self.new_note_text.pack(fill="x")
        add_button = ttk.Button(add_note_frame, text="Add Note", command=self.add_note)
        add_button.pack(pady=5)
        self.add_note_button = add_button

        self.feedback_label = ttk.Label(self, text="", foreground="green")
        self.feedback_label.pack(pady=5)

    def apply_permissions(self):
        if self.logged_in_role == "Customer Service Agent":
            # Agents can search, view accounts and transactions, and add notes
            if hasattr(self, 'search_button'):
                self.search_button.config(state="normal")
            if hasattr(self, 'add_note_button'):
                self.add_note_button.config(state="normal")
            if hasattr(self, 'new_note_text'):
                self.new_note_text.config(state="normal")
        elif self.logged_in_role == "Administrator":
            # Admins have full access (for now)
            if hasattr(self, 'search_button'):
                self.search_button.config(state="normal")
            if hasattr(self, 'add_note_button'):
                self.add_note_button.config(state="normal")
            if hasattr(self, 'new_note_text'):
                self.new_note_text.config(state="normal")
        else:
            # For other roles or no role, disable interactive elements
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button):
                    widget.config(state="disabled")
                elif isinstance(widget, ttk.Entry):
                    widget.config(state="disabled")
                elif isinstance(widget, tk.Text):
                    widget.config(state="disabled")
            messagebox.showerror("Access Denied", "Your role does not have sufficient permissions to access this window.")
            self.destroy()

    def search_accounts(self):
        search_term = self.account_search_entry.get()
        account = self.account_service.get_account_details(search_term)
        if account:
            for item in self.account_list.get_children():
                self.account_list.delete(item)
            self.account_list.insert("", tk.END, values=(account.account_id, account.type, account.balance))
            self.current_account = account
            self.load_transactions(None)
            self.update_account_details()
        else:
            self.clear_account_details()
            self.feedback_label.config(text="Account not found.", foreground="red")
            self.after(3000, lambda: self.feedback_label.config(text=""))

    def load_transactions(self, event):
        if self.current_account:
            transactions = self.transaction_service.get_transactions_by_account(self.current_account.account_id)
            for item in self.transaction_list.get_children():
                self.transaction_list.delete(item)
            for transaction in transactions:
                self.transaction_list.insert("", tk.END, values=(transaction.transaction_id, transaction.type, transaction.amount, transaction.timestamp, transaction.status))
            self.update_account_details()
        else:
            for item in self.transaction_list.get_children():
                self.transaction_list.delete(item)
            self.clear_account_details()

    def update_account_details(self):
        if self.current_account:
            self.account_type_label.config(text=f"Type: {self.current_account.type}")
            self.account_balance_label.config(text=f"Balance: {self.current_account.balance}")
        else:
            self.clear_account_details()

    def clear_account_details(self):
        self.account_type_label.config(text="Type:")
        self.account_balance_label.config(text="Balance:")

    def display_notes(self):
        self.notes_text.config(state="normal")
        self.notes_text.delete("1.0", tk.END)
        if hasattr(self.current_account, 'notes') and self.current_account.notes:
            for note_entry in self.current_account.notes:
                timestamp = note_entry.get('timestamp', 'N/A')
                note = note_entry.get('note', '')
                self.notes_text.insert(tk.END, f"[{timestamp}] {note}\n")
        self.notes_text.config(state="disabled")

    def add_note(self):
        if self.current_account and self.logged_in_role in ["Customer Service Agent", "Administrator"]:
            note = self.new_note_text.get("1.0", tk.END).strip()
            if note:
                now = datetime.now()
                new_note = {"timestamp": now.strftime("%Y-%m-%d %H:%M:%S"), "note": note}
                if not hasattr(self.current_account, 'notes'):
                    self.current_account.notes = []
                self.current_account.notes.append(new_note)
                self.display_notes()
                try:
                    self.account_service.save_account(self.current_account)
                    self.feedback_label.config(text="Note added successfully!", foreground="green")
                    self.after(3000, lambda: self.feedback_label.config(text=""))
                    self.new_note_text.delete("1.0", tk.END)
                except Exception as e:
                    self.feedback_label.config(text=f"Error saving note: {e}", foreground="red")
            else:
                self.feedback_label.config(text="Please enter a note.", foreground="red")
                self.after(3000, lambda: self.feedback_label.config(text=""))
        elif not self.current_account:
            self.feedback_label.config(text="No account selected.", foreground="red")
            self.after(3000, lambda: self.feedback_label.config(text=""))
        else:
            messagebox.showerror("Permission Denied", "Your role is not allowed to add notes.")