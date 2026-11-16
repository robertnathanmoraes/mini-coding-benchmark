import re

_PATTERN = re.compile(r"[A-Z]{3}-?[0-9][A-Z0-9][0-9]{2}")


def is_valid_plate(plate) -> bool:
    if not isinstance(plate, str):
        return False
    return _PATTERN.fullmatch(plate.upper()) is not None
