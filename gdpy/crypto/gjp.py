import hashlib

from gdpy.constants import Salts


def generate_gjp2(password: str) -> str:
    salted = password + Salts.GJP2
    return hashlib.sha1(salted.encode()).hexdigest()
