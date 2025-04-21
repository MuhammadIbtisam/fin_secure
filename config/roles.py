roles = {
    "administrator": ["read_all", "create", "update", "delete", "manage_roles"],
    "branch_manager": ["read_customer", "read_account", "read_transaction", "generate_reports"],
    "customer_service": ["read_customer", "update_customer_contact", "read_account_summary"],
    "auditor": ["read_all_logs", "read_compliance"]
}