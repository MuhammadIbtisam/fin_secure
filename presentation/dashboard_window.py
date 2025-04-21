
import tkinter as tk
from tkinter import ttk

class DashboardWindow(tk.Toplevel):
    def __init__(self, parent, dashboard_stats_service):
        super().__init__(parent)
        self.title("Staff Management Dashboard")
        self.geometry("800x600")
        self.dashboard_stats_service = dashboard_stats_service

        # Financial Metrics Frame
        financial_frame = ttk.LabelFrame(self, text="Financial Metrics")
        financial_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(financial_frame, text=f"Total Assets: {self.dashboard_stats_service.calculate_total_assets()}").pack(pady=2, anchor="w")
        ttk.Label(financial_frame, text=f"Total Liabilities: {self.dashboard_stats_service.calculate_total_liabilities()}").pack(pady=2, anchor="w")
        ttk.Label(financial_frame, text=f"Net Worth: {self.dashboard_stats_service.calculate_net_worth()}").pack(pady=2, anchor="w")
        ttk.Label(financial_frame, text=f"Total Revenue: {self.dashboard_stats_service.calculate_total_revenue()}").pack(pady=2, anchor="w")
        ttk.Label(financial_frame, text=f"Total Expenses: {self.dashboard_stats_service.calculate_total_expenses()}").pack(pady=2, anchor="w")

        # Customer Insights Frame
        customer_frame = ttk.LabelFrame(self, text="Customer Insights")
        customer_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(customer_frame, text=f"Total Customers: {self.dashboard_stats_service.get_total_customers()}").pack(pady=2, anchor="w")
        ttk.Label(customer_frame, text=f"New Customers: {self.dashboard_stats_service.get_new_customers('some_date')}").pack(pady=2, anchor="w")
        ttk.Label(customer_frame, text=f"Customer Satisfaction: {self.dashboard_stats_service.get_customer_satisfaction_score()}").pack(pady=2, anchor="w")
        ttk.Label(customer_frame, text=f"Churn Rate: {self.dashboard_stats_service.get_churn_rate()}").pack(pady=2, anchor="w")

        # Transaction Monitoring Frame
        transaction_frame = ttk.LabelFrame(self, text="Transaction Monitoring")
        transaction_frame.pack(padx=10, pady=10, fill="x")
        ttk.Label(transaction_frame, text=f"Total Transactions: {self.dashboard_stats_service.get_total_transactions()}").pack(pady=2, anchor="w")
        ttk.Label(transaction_frame, text=f"Fraudulent Transactions: {self.dashboard_stats_service.get_fraudulent_transactions()}").pack(pady=2, anchor="w")
        ttk.Label(transaction_frame, text=f"Transaction Volume: {self.dashboard_stats_service.get_transaction_volume()}").pack(pady=2, anchor="w")
        ttk.Label(transaction_frame, text=f"Success Rate: {self.dashboard_stats_service.get_transaction_success_rate():.2f}%").pack(pady=2, anchor="w")

        # Regulatory Compliance Frame
        compliance_frame = ttk.LabelFrame(self, text="Regulatory Compliance")
        compliance_frame.pack(padx=10, pady=10, fill="x")
        compliance_summary = self.dashboard_stats_service.get_compliance_status_summary()
        ttk.Label(compliance_frame, text=f"Compliant Regulations: {compliance_summary['compliant']}").pack(pady=2, anchor="w")
        ttk.Label(compliance_frame, text=f"Non-Compliant Regulations: {compliance_summary['non_compliant']}").pack(pady=2, anchor="w")
        audit_logs = self.dashboard_stats_service.get_latest_audit_logs()
        ttk.Label(compliance_frame, text=f"Latest Audit Logs: {', '.join(audit_logs)}").pack(pady=2, anchor="w")
