from app.customers.services import CustomerService
from app.accounts.services import AccountService, TransactionService
from app.compliance.services import ComplianceService

class DashboardStatsService:
    def __init__(self, customer_service: CustomerService, account_service: AccountService,
                 transaction_service: TransactionService, compliance_service: ComplianceService):
        self.customer_service = customer_service
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.compliance_service = compliance_service

    def calculate_total_assets(self) -> float:
        total_assets = 0
        accounts = self.account_service.account_repository.get_all()
        for account in accounts:
            if account.type in ['savings', 'checking']:
                total_assets += account.balance
        return total_assets

    def calculate_total_liabilities(self) -> float:
        total_liabilities = 0
        accounts = self.account_service.account_repository.get_all()
        for account in accounts:
            if account.type == 'loan' and account.balance < 0:
                total_liabilities += abs(account.balance)
        return total_liabilities

    def calculate_net_worth(self) -> float:
        return self.calculate_total_assets() - self.calculate_total_liabilities()

    def calculate_total_revenue(self) -> float:
        return 0.0

    def calculate_total_expenses(self) -> float:
        return 0.0

    def get_total_customers(self) -> int:
        return len(self.customer_service.get_all_customers())

    def get_new_customers(self, since_date) -> int:
        return self.get_total_customers()

    def get_customer_satisfaction_score(self) -> float:
        return 0.0

    def get_churn_rate(self) -> float:
        return 0.0

    def get_total_transactions(self) -> int:
        return len(self.transaction_service.transaction_repository.get_all())

    def get_fraudulent_transactions(self) -> int:
        fraudulent_count = 0
        all_transactions = self.transaction_service.transaction_repository.get_all()
        for transaction in all_transactions:
            if transaction.status == 'flagged_fraud':
                fraudulent_count += 1
        return fraudulent_count

    def get_transaction_volume(self) -> float:
        total_volume = 0
        all_transactions = self.transaction_service.transaction_repository.get_all()
        for transaction in all_transactions:
            if transaction.status == 'success':
                total_volume += transaction.amount
        return total_volume

    def get_transaction_success_rate(self) -> float:
        total_transactions = self.get_total_transactions()
        if total_transactions == 0:
            return 0.0
        successful_transactions = sum(1 for t in self.transaction_service.transaction_repository.get_all() if t.status == 'success')
        return (successful_transactions / total_transactions) * 100

    def get_compliance_status_summary(self) -> dict:
        summary = {"compliant": 0, "non_compliant": 0}
        regulations = self.compliance_service.get_all_regulations()
        for reg in regulations:
            if reg.status == 'compliant':
                summary["compliant"] += 1
            elif reg.status == 'non-compliant':
                summary["non_compliant"] += 1
        return summary

    def get_latest_audit_logs(self) -> list:
        return ["Regulatory change tracked for KYC-2024", "Regulatory change tracked for AML-2025"]

    def get_customers_by_segment_counts(self):
        customers = self.customer_service.get_all_customers()
        segment_counts = {}
        for customer in customers:
            segment = customer.customer_segment if customer.customer_segment is not None else "Unknown Segment"
            segment_counts[segment] = segment_counts.get(segment, 0) + 1
        print(f"Segment counts: {segment_counts}")
        return segment_counts

    # customers = self.customer_service.get_all_customers()
    # segment_counts = {}
    # for customer in customers:
    #     segment = customer.customer_segment
    #     if segment:
    #         segment_counts[segment] = segment_counts.get(segment, 0) + 1
    #
    # print(f"Segment counts: {segment_counts}")
    # return segment_counts