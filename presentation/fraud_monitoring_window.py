import tkinter as tk
from tkinter import ttk

class FraudMonitoringWindow(tk.Toplevel):
    def __init__(self, parent, transaction_service):
        super().__init__(parent)
        self.title("Fraud Monitoring")
        self.geometry("1400x900")
        self.transaction_service = transaction_service

        # Account Selection Frame
        account_frame = ttk.LabelFrame(self, text="Monitor Account")
        account_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(account_frame, text="Account ID:").pack(side="left", padx=5)
        self.account_entry = ttk.Entry(account_frame)
        self.account_entry.pack(side="left", padx=5, fill="x", expand=True)
        monitor_button = ttk.Button(account_frame, text="Monitor Account", command=self.monitor_fraud)
        monitor_button.pack(side="left", padx=5)

        # Fraudulent Transactions List Frame
        fraud_list_frame = ttk.LabelFrame(self, text="Potentially Fraudulent Transactions")
        fraud_list_frame.pack(padx=10, pady=10, fill="both", expand=True)
        self.fraud_list = ttk.Treeview(fraud_list_frame, columns=("ID", "Account", "Type", "Amount", "Timestamp", "Reason", "Status"), show="headings")
        self.fraud_list.heading("ID", text="Transaction ID")
        self.fraud_list.heading("Account", text="Account ID")
        self.fraud_list.heading("Type", text="Type")
        self.fraud_list.heading("Amount", text="Amount")
        self.fraud_list.heading("Timestamp", text="Timestamp")
        self.fraud_list.heading("Reason", text="Reason for Flagging")
        self.fraud_list.heading("Status", text="Status")
        self.fraud_list.pack(fill="both", expand=True)

    def monitor_fraud(self):
        account_id = self.account_entry.get()
        if account_id:
            fraudulent_transactions = self.transaction_service.identify_potential_fraud(account_id)
            for item in self.fraud_list.get_children():
                self.fraud_list.delete(item)
            for transaction in fraudulent_transactions:
                # Assuming your identify_potential_fraud now returns transactions with a 'fraud_reason' attribute
                self.fraud_list.insert("", tk.END, values=(
                    transaction.transaction_id,
                    transaction.account_id,
                    transaction.type,
                    transaction.amount,
                    transaction.timestamp,
                    getattr(transaction, 'fraud_reason', 'N/A'), # Get reason, default to 'N/A' if not present
                    transaction.status
                ))
        else:
            ttk.Label(self, text="Please enter an Account ID.", foreground="red").pack()