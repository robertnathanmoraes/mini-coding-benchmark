# Task 001 - Brazilian license plate validator

Write a Python function:

```python
def is_valid_plate(plate) -> bool:
```

Return `True` if `plate` is a valid Brazilian license plate, otherwise `False`.

Valid formats (after normalization):

- Old format: 3 letters + 4 digits, e.g. `ABC1234`
- Mercosul format: 3 letters + 1 digit + 1 letter + 2 digits, e.g. `ABC1D23`

Normalization rules:

- Letters may be lowercase (`abc1234` is valid).
- A single hyphen between the letters and the numbers is allowed (`ABC-1234`, `ABC-1D23`).
- Any other character (spaces, dots, extra hyphens) makes the plate invalid.

If `plate` is not a string, return `False` (do not raise).

Examples:

| Input | Output |
| --- | --- |
| `"ABC1234"` | `True` |
| `"abc-1d23"` | `True` |
| `"AB12345"` | `False` |
| `"ABC 1234"` | `False` |
| `None` | `False` |

Write the solution in a single file `solution.py`.
