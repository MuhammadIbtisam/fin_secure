import json
from typing import List
from app.customers.models import Customer, ContactInfo, Interaction, AccountSummaryItem
from app.utils.data_manager import load_json, save_json
import os

class CustomerRepository:
    def __init__(self, data_file='customers.json'):
        self.data_file = data_file
        self.customers = self._load_customers()

    def _load_customers(self) -> List[Customer]:
        customer_data_list = load_json(self.data_file)
        customers = []
        for customer_data in customer_data_list:
            contact_info_data = customer_data.get('contact_info', {})
            contact_info = ContactInfo(
                email=contact_info_data.get('email'),
                phone=contact_info_data.get('phone')
            )

            interaction_log_data = customer_data.get('interaction_log', [])
            interaction_log = [
                Interaction(
                    date=interaction.get('date'),
                    type=interaction.get('type'),
                    notes=interaction.get('notes')
                )
                for interaction in interaction_log_data
            ]

            account_summary_data = customer_data.get('account_summary', {})
            account_summary = {
                account_id: AccountSummaryItem(
                    type=summary.get('type'),
                    balance=summary.get('balance')
                )
                for account_id, summary in account_summary_data.items()
            }

            customer = Customer(
                customer_id=customer_data.get('customer_id'),
                name=customer_data.get('name'),
                password=customer_data.get('password'),
                contact_info=contact_info,
                account_ids=customer_data.get('account_ids', []),
                account_summary=account_summary,
                products=customer_data.get('products', []),
                interaction_log=interaction_log,
                last_interaction_date=customer_data.get('last_interaction_date'),
                total_interactions=customer_data.get('total_interactions', 0),
                advice_history=customer_data.get('advice_history', []),
                personalized_advice=customer_data.get('personalized_advice', []),
                date_of_birth=customer_data.get('date_of_birth'),
                address=customer_data.get('address'),
                customer_segment=customer_data.get('customer_segment'),
                consent=customer_data.get('consent')
            )
            customers.append(customer)
        return customers

    def get_all(self) -> List[Customer]:
        return self.customers

    def get_by_id(self, customer_id: str):
        for customer in self.customers:
            if customer.customer_id == customer_id:
                return customer
        return None

    def get_by_name(self, name: str):
        for customer in self.customers:
            if customer.name == name:
                return customer
        return None

    def get_by_account_id(self, account_id: str) -> List[Customer]:
        matching_customers = [
            customer for customer in self.customers if account_id in customer.account_ids
        ]
        return matching_customers

    def get_by_product(self, product_name: str) -> List[Customer]:
        matching_customers = [
            customer for customer in self.customers if product_name in customer.products
        ]
        return matching_customers

    def get_by_segment(self, segment: str) -> List[Customer]:
        matching_customers = [
            customer for customer in self.customers if customer.customer_segment == segment
        ]
        return matching_customers

    def get_by_last_interaction_date(self, date: str) -> List[Customer]:
        matching_customers = [
            customer for customer in self.customers if customer.last_interaction_date == date
        ]
        return matching_customers

    def update(self, customer_to_update: Customer):
        for i, customer in enumerate(self.customers):
            if customer.customer_id == customer_to_update.customer_id:
                self.customers[i] = customer_to_update
                self._save_customers()
                return

    def _save_customers(self):
        data_to_save = []
        for customer in self.customers:
            customer_data = customer.__dict__.copy()
            customer_data['contact_info'] = customer.contact_info.__dict__
            account_summary_data = {}
            for account_id, summary_item in customer_data.get('account_summary', {}).items():
                account_summary_data[account_id] = summary_item.__dict__
            customer_data['account_summary'] = account_summary_data

            interaction_log_data = []
            for interaction in customer.interaction_log:
                interaction_log_data.append(interaction.__dict__)
            customer_data['interaction_log'] = interaction_log_data

            data_to_save.append(customer_data)
        save_json(self.data_file, data_to_save)

    def add_customer(self, customer: Customer):
        self.customers.append(customer)
        self._save_customers()

    def delete_customer(self, customer_id: str):
        """Deletes a customer from the repository."""
        initial_len = len(self.customers)
        self.customers = [customer for customer in self.customers if customer.customer_id != customer_id]
        if len(self.customers) < initial_len:
            self._save_customers()
            return True
        return False
