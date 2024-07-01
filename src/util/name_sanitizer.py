"""
Defines a function that sanitizes a name by removing all non-alphanumeric characters.
"""

def sanitize_name(name: str) -> str:
    name = (
        name.replace(" +", "")
        .replace("+", "")
        .replace(" ", "_")
        .replace("-", "_")
        .replace("(", "")
        .replace(")", "")
        .rsplit(".", 1)[0]
    )

    return name
