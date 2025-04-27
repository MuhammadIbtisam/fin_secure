from app.customers.repository import CustomerRepository
from app.accounts.repository import AccountRepository, TransactionRepository
from app.customers.services import CustomerService
from app.accounts.services import AccountService, TransactionService
# from app.accounts.models import Interaction

def main():
    customer_repository = CustomerRepository()
    account_repository = AccountRepository()
    transaction_repository = TransactionRepository()

    account_service = AccountService(account_repository, transaction_repository)
    customer_service = CustomerService(customer_repository, account_service)
    transaction_service = TransactionService(transaction_repository, account_repository)

    print('I am here 1')
    customer = customer_service.get_customer_profile("C001")
    if customer:
        print(f"Customer Name: {customer.name}")
        accounts = customer_service.get_customer_accounts(customer.customer_id)
        if accounts:
            print("\nAccounts:")
            for account in accounts:
                print(f"- Account ID: {account.account_id}, Type: {account.type}, Balance: {account.balance}")
        else:
            print("\nNo accounts found for this customer.")

    transactions = transaction_service.get_transactions_by_account("A001")
    if transactions:
        print("\nTransactions for Account A001:")
        for transaction in transactions:
            print(f"- ID: {transaction.transaction_id}, Type: {transaction.type}, Amount: {transaction.amount}, Status: {transaction.status}")

    potential_fraud = transaction_service.identify_potential_fraud("A001")
    if potential_fraud:
        print("\nPotential Fraudulent Transactions for Account A001:")
        for transaction in potential_fraud:
            print(f"- ID: {transaction.transaction_id}, Type: {transaction.type}, Amount: {transaction.amount}, Status: {transaction.status}")

if __name__ == "__main__":
    main()