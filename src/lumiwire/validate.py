"""Validate a hex-encoded ISO 8583:1987 message against a spec."""
from .decode import DecodeError, decode
from .spec import Spec

_DIGITS = "0123456789"
_Z_SEPARATORS = "=D"


def _bad_char(kind: str, value: str) -> str | None:
    """Return a description of the first character not allowed for `kind`, or None."""
    for c in value:
        if kind == "n" and c not in _DIGITS:
            return "non-digit"
        if kind == "an" and not (c.isascii() and c.isalnum()):
            return "non-alphanumeric"
        if kind == "ans" and not 0x20 <= ord(c) <= 0x7E:
            return "non-printable"
        if kind == "z" and c not in _DIGITS + _Z_SEPARATORS:
            return "invalid"
    return None


def validate(hex_message: str, spec: Spec) -> list[str]:
    try:
        message = decode(hex_message, spec)
    except DecodeError as e:
        return [str(e)]
    errors = []
    mti = message["mti"]
    if len(mti) != 4 or not all(c in _DIGITS for c in mti):
        errors.append(f"MTI {mti!r}: must be 4 digits")
    elif mti[0] != "0":
        errors.append(f"MTI {mti!r}: version digit must be 0 for ISO 8583:1987")
    for num, value in message["fields"].items():
        f = spec.fields[num]
        label = f"field {num} ({f.name})"
        if len(value) > f.max:
            errors.append(f"{label}: length {len(value)} exceeds max {f.max}")
        problem = _bad_char(f.type, value)
        if problem:
            # never quote the value of a PAN or track field
            c = next(c for c in value if _bad_char(f.type, c))
            shown = "" if f.sensitive else f" {c!r}"
            errors.append(f"{label}: {problem} character{shown} in {f.type} field")
    return errors
