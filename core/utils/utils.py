from ..allowed_domains import allowed_domains
def verify_email(email: str) -> bool:
    """
    Verifies if the provided email address is valid.
    """
    if "@" not in email:
        return False
    
    domain = email.split("@")[1]
    return domain in allowed_domains