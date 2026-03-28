from typing import Any


def parse_response(response: str) -> dict[str, Any]:
    if response in ("-1", "-2") or response.startswith("-"):
        return {"_error": int(response)}
    result: dict[str, Any] = {}
    for pair in response.split("|"):
        parts = pair.split(":")
        for i in range(0, len(parts) - 1, 2):
            key = parts[i]
            value = parts[i + 1]
            result[key] = value
    return result


def parse_list_response(response: str, delimiter: str = "|") -> list[dict[str, Any]]:
    if response == "-1" or response == "-2":
        return []
    return [parse_response(obj) for obj in response.split(delimiter) if obj]
