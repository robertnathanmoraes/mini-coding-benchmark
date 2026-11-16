# Hand-written "naive" answer used to demonstrate the evaluator.
# It is NOT output from a real model. Typical mistake: checks only length and
# a loose regex, and crashes on non-string input.
import re


def is_valid_plate(plate) -> bool:
    plate = plate.upper().replace("-", "")
    return len(plate) == 7 and re.match(r"[A-Z]{3}\d", plate) is not None
