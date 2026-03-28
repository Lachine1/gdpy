import hashlib


def generate_chk(data: str, salt: str) -> str:
    combined = data + salt
    return hashlib.sha1(combined.encode()).hexdigest()
