
from typing import List, Optional
from app.customers.models import Customer,  Interaction
from app.customers.repository import CustomerRepository
from app.accounts.services import AccountService
from app.utils.data_manager import save_json

class CustomerService:
    def __init__(self, customer_repository: CustomerRepository, account_service: AccountService):
        self.customer_repository = customer_repository
        self.account_service = account_service

    def get_customer_profile(self, customer_id: str) -> Optional[Customer]:
        customer =  self.customer_repository.get_by_id(customer_id)
        print(f"Customer Name: {customer.name}")
        print('I am here 3=4')
        return customer

    def get_all_customers(self) -> List[Customer]:
        return self.customer_repository.get_all()

    def get_customers_by_account(self, account_id: str) -> List[Customer]:
        return self.customer_repository.get_by_account_id(account_id)

    def get_customers_by_product(self, product_name: str) -> List[Customer]:
        return self.customer_repository.get_by_product(product_name)

    def get_customers_by_segment(self, segment: str) -> List[Customer]:
        return self.customer_repository.get_by_segment(segment)

    def update_interaction_log(self, customer_id: str, interaction: Interaction) -> Optional[Customer]:
        customer = self.customer_repository.get_by_id(customer_id)
        if customer:
            customer.interaction_log.append(interaction)
            customer.total_interactions = len(customer.interaction_log)  # Update total interactions
            self._save_customers()  # Save the updated customer data
            return customer
        return None

    def provide_personalized_advice(self, customer: Customer) -> List[str]:
        advice = []

        # Basic rules-based advice (you can expand these significantly)
        if "Savings Account" in customer.products and customer.account_summary.get("A001") and customer.account_summary[
            "A001"].balance < 1000:
            advice.append("Consider increasing your savings to reach your financial goals.")

        if "Personal Loan" in customer.products and customer.account_summary.get("A002") and customer.account_summary[
            "A002"].balance < -5000:
            advice.append("Review your loan repayment options to manage your debt effectively.")

        if customer.customer_segment == "New Customer" and customer.total_interactions < 3:
            advice.append("Schedule a follow-up call to discuss our full range of services.")
        return advice

    def _save_customers(self):
        customer_data_list = []
        for customer in self.customer_repository.customers:
            customer_data = {
                "customer_id": customer.customer_id,
                "name": customer.name,
                "contact_info": {
                    "email": customer.contact_info.email,
                    "phone": customer.contact_info.phone
                },
                "account_ids": customer.account_ids,
                "account_summary": {
                    account_id: {"type": summary.type, "balance": summary.balance}
                    for account_id, summary in customer.account_summary.items()
                },
                "products": customer.products,
                "interaction_log": [
                    {"date": interaction.date, "type": interaction.type, "notes": interaction.notes}
                    for interaction in customer.interaction_log
                ],
                "last_interaction_date": customer.last_interaction_date,
                "total_interactions": customer.total_interactions,
                "advice_history": customer.advice_history,
                "personalized_advice": customer.personalized_advice,
                "date_of_birth": customer.date_of_birth,
                "address": customer.address,
                "customer_segment": customer.customer_segment,
                "consent": customer.consent
            }
            customer_data_list.append(customer_data)

        save_json(self.customer_repository.data_file, customer_data_list)

    def get_customer_accounts(self, customer_id: str):
        customer = self.customer_repository.get_by_id(customer_id)
        if customer:
            accounts = []
            for account_id in customer.account_ids:
                account = self.account_service.get_account_details(account_id)
                if account:
                    accounts.append(account)
            return accounts
        return []