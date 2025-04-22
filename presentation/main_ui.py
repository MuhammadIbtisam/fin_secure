import os
import tkinter as tk
from tkinter import ttk
from app.customers.repository import CustomerRepository
from app.accounts.repository import AccountRepository, TransactionRepository
from app.customers.services import CustomerService
from app.accounts.services import AccountService, TransactionService
from app.dashboard.stats import DashboardStatsService
from presentation.login_window import LoginWindow
from presentation.customers_management_window import CustomersManagementWindow
from presentation.accounts_window import AccountsWindow
from presentation.dashboard_window import DashboardWindow
from presentation.fraud_monitoring_window import FraudMonitoringWindow
from app.compliance.repository import ComplianceRepository
from app.compliance.services import ComplianceService


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("FinSecure Application")
        self.geometry("800x600")
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        data_dir = os.path.join(base_dir, 'data')
        customers_file_path = os.path.join(data_dir, 'customers.json')
        accounts_file_path = os.path.join(data_dir, 'accounts.json')
        transactions_file_path = os.path.join(data_dir, 'transactions.csv')
        compliance_file_path = os.path.join(data_dir, 'regulations.json')

        # Instantiate repositories with just the filenames
        self.customer_repository = CustomerRepository(data_file=customers_file_path)
        self.account_repository = AccountRepository(data_file=accounts_file_path)
        self.transaction_repository = TransactionRepository(data_file=transactions_file_path)
        self.compliance_repository = ComplianceRepository(data_file=compliance_file_path)

        # Instantiate services
        self.account_service = AccountService(self.account_repository, self.transaction_repository)
        self.customer_service = CustomerService(self.customer_repository, self.account_service)
        self.transaction_service = TransactionService(self.transaction_repository)
        self.compliance_service = ComplianceService(self.compliance_repository)
        self.dashboard_stats_service = DashboardStatsService(
            self.customer_service, self.account_service, self.transaction_service, self.compliance_service
            # Compliance service might be needed later
        )

        self.show_login()
        self.main_frame = None

    def show_login(self):
        self.login_window = LoginWindow(self, self.login_successful)

    def login_successful(self):
        if self.login_window:
            self.login_window.destroy()
        self.show_main_interface()

    def show_main_interface(self):
        if self.main_frame:
            self.main_frame.destroy()

        self.main_frame = ttk.Frame(self, padding=10)
        self.main_frame.pack(expand=True, fill="both")

        customer_button = ttk.Button(self.main_frame, text="Customer Management", command=self.show_customer_management)
        customer_button.pack(pady=10)

        accounts_button = ttk.Button(self.main_frame, text="Accounts", command=self.show_accounts)
        accounts_button.pack(pady=10)

        dashboard_button = ttk.Button(self.main_frame, text="Dashboard", command=self.show_dashboard)
        dashboard_button.pack(pady=10)

        fraud_button = ttk.Button(self.main_frame, text="Fraud Monitoring", command=self.show_fraud_monitoring)
        fraud_button.pack(pady=10)

    def show_customer_management(self):
        CustomersManagementWindow(self, self.customer_service)

    def show_accounts(self):
        AccountsWindow(self, self.account_service, self.transaction_service)

    def show_dashboard(self):
        DashboardWindow(self, self.dashboard_stats_service)

    def show_fraud_monitoring(self):
        FraudMonitoringWindow(self, self.transaction_service)
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()