from config.roles import roles

def check_permission(user_role: str, permission_needed: str) -> bool:
    if user_role in roles and permission_needed in roles[user_role]:
        return True
    return False
