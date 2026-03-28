def xor_cipher(data: str, key: str) -> str:
    result = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        result.append(chr(ord(char) ^ ord(key_char)))
    return "".join(result)


def xor_cipher_int(data: str, key: int) -> str:
    result = []
    for char in data:
        result.append(chr(ord(char) ^ key))
    return "".join(result)
