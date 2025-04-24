
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

class DashboardWindow(tk.Toplevel):
    def __init__(self, parent, dashboard_stats_service):
        super().__init__(parent)
        self.title("Staff Management Dashboard")
        self.geometry("1600x900")
        self.dashboard_stats_service = dashboard_stats_service
        self.init_dashboard()

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

    def init_dashboard(self):
        customer_segment_data = self.dashboard_stats_service.get_customers_by_segment_counts()
        print(f"Data from service: {customer_segment_data}")
        if customer_segment_data:
            fig_customers, ax_customers = plt.subplots(figsize=(6, 4))
            segments = list(customer_segment_data.keys())
            counts = list(customer_segment_data.values())
            ax_customers.bar(segments, counts)
            ax_customers.set_xlabel("Customer Segment")
            ax_customers.set_ylabel("Number of Customers")
            ax_customers.set_title("Customers by Segment")

            canvas_customers = FigureCanvasTkAgg(fig_customers, master=self)
            canvas_widget_customers = canvas_customers.get_tk_widget()
            canvas_widget_customers.pack(fill=tk.BOTH, expand=True)

            toolbar_customers = NavigationToolbar2Tk(canvas_customers, self)
            toolbar_customers.update()
            toolbar_customers.pack(fill=tk.X)
            canvas_customers.draw()

    # def init_dashboard(self):
    #     fig, ax = plt.subplots()
    #     ax.plot([1, 2, 3, 4], [5, 6, 7, 8])
    #     canvas = FigureCanvasTkAgg(fig, master=self)
    #     canvas_widget = canvas.get_tk_widget()
    #     canvas_widget.pack(fill=tk.BOTH, expand=True)
    #     canvas.draw()
