import base64
import hashlib
import random


def generate_chk(data: str, salt: str) -> str:
    combined = data + salt
    return hashlib.sha1(combined.encode()).hexdigest()


def generate_rewards_chk(key: str = "59182") -> str:
    """Generate chk parameter for rewards endpoints.

    Args:
        key: XOR key to use (19847 for challenges, 59182 for chest rewards)

    Returns:
        The chk parameter string.
    """
    random_string = "".join(
        random.choice("1234567890qwertyuiopaqsdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM")
        for _ in range(5)
    )
    random_number = str(random.randint(10000, 1000000))
    xor_result = "".join(
        chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(random_number)
    )
    encoded = base64.b64encode(xor_result.encode()).decode()
    return random_string + encoded


def decode_rewards_response(response: str, key: str = "59182") -> str:
    """Decode the XOR'd and base64 encoded rewards response.

    Args:
        response: The response from the server.
        key: XOR key to use for decoding.

    Returns:
        The decoded response string.
    """
    # Remove the 5 random chars at the start and split by |
    encoded_part = response.split("|")[0][5:]
    decoded = base64.urlsafe_b64decode(encoded_part.encode()).decode()
    return "".join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(decoded))
