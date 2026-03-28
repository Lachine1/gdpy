"""XOR cipher implementations for Geometry Dash encoding.

The XOR cipher is used throughout Geometry Dash for various
encoding purposes, including level passwords and other data.
"""


def xor_cipher(data: str, key: str) -> str:
    """Apply XOR cipher to data using a string key.

    Each character in the data is XOR'd with the corresponding
    character in the key, cycling through the key as needed.

    Args:
        data: The string to encode/decode.
        key: The key to use for XOR operation.

    Returns:
        The XOR'd result string.

    Example:
        ```python
        encoded = xor_cipher("hello", "key")
        decoded = xor_cipher(encoded, "key")  # Returns "hello"
        ```
    """
    result = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        result.append(chr(ord(char) ^ ord(key_char)))
    return "".join(result)


def xor_cipher_int(data: str, key: int) -> str:
    """Apply XOR cipher to data using an integer key.

    Each character in the data is XOR'd with the key value.

    Args:
        data: The string to encode/decode.
        key: The integer key to use for XOR operation.

    Returns:
        The XOR'd result string.

    Example:
        ```python
        encoded = xor_cipher_int("hello", 11)
        decoded = xor_cipher_int(encoded, 11)  # Returns "hello"
        ```
    """
    result = []
    for char in data:
        result.append(chr(ord(char) ^ key))
    return "".join(result)
