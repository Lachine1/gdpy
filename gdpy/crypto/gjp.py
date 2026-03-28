"""GJP2 password encoding for Geometry Dash authentication.

GJP2 (Geometry Jump Password 2) is the hashing algorithm used
for encoding passwords when communicating with the Geometry Dash servers.
"""

import hashlib

from gdpy.constants import Salts


def generate_gjp2(password: str) -> str:
    """Generate a GJP2 hash from a password.
    
    GJP2 is used for authenticating with the Geometry Dash API.
    The password is salted with a fixed string and hashed using SHA-1.
    
    Args:
        password: The plaintext password to hash.
    
    Returns:
        A 40-character hexadecimal SHA-1 hash string.
    
    Example:
        ```python
        gjp2_hash = generate_gjp2("my_password")
        # Returns a 40-character hex string
        ```
    """
    salted = password + Salts.GJP2
    return hashlib.sha1(salted.encode()).hexdigest()
