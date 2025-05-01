from typing import Dict, List, Optional


class ContactInfo:
    def __init__(self, email: str, phone: str):
        self.email = email
        self.phone = phone


class Interaction:
    def __init__(self, date: str, type: str, notes: str):
        self.date = date
        self.type = type
        self.notes = notes


class AccountSummaryItem:
    def __init__(self, type: str, balance: float):
        self.type = type
        self.balance = balance


class Customer:
    def __init__(self, customer_id: str, name: str, contact_info: ContactInfo,
                 account_ids: List[str], account_summary: Dict[str, AccountSummaryItem],
                 products: List[str], interaction_log: List[Interaction],
                 last_interaction_date: Optional[str], total_interactions: int,
                 advice_history: List[str], personalized_advice: List[str],
                 password: str,
                 date_of_birth: Optional[str] = None,
                 address: Optional[str] = None,
                 customer_segment: Optional[str] = None,
                 consent: Optional[Dict[str, bool]] = None):
        self.customer_id = customer_id
        self.password = password
        self.name = name
        self.contact_info = contact_info
        self.account_ids = account_ids
        self.account_summary = account_summary
        self.products = products
        self.interaction_log = interaction_log
        self.last_interaction_date = last_interaction_date
        self.total_interactions = total_interactions
        self.advice_history = advice_history
        self.personalized_advice = personalized_advice
        self.date_of_birth = date_of_birth
        self.address = address
        self.customer_segment = customer_segment
        self.consent = consent
