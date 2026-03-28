import base64


def encode_base64(data: str) -> str:
    encoded = base64.b64encode(data.encode()).decode()
    return encoded.replace("+", "-").replace("/", "_")


def decode_base64(data: str) -> str:
    data = data.replace("-", "+").replace("_", "/")
    padding = 4 - len(data) % 4
    if padding != 4:
        data += "=" * padding
    return base64.b64decode(data.encode()).decode(errors="replace")
