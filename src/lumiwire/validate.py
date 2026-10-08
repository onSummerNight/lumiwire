"""Validate a hex-encoded ISO 8583:1987 message against a spec."""
from .decode import DecodeError, _Reader, _read_digits, decode
from .spec import EDITIONS, Spec

_DIGITS = "0123456789"
_Z_SEPARATORS = "=D"
_HEX = "0123456789abcdefABCDEF"


def _bad_char(kind: str, value: str) -> str | None:
    """Return a description of the first character not allowed for `kind`, or None."""
    for c in value:
        if kind == "n" and c not in _DIGITS:
            return "non-digit"
        if kind == "an" and not (c.isascii() and c.isalnum()):
            return "non-alphanumeric"
        if kind == "ans" and not 0x20 <= ord(c) <= 0x7E:
            return "non-printable"
        if kind == "b" and c not in _HEX:
            return "non-hex"
        if kind == "z" and c not in _DIGITS + _Z_SEPARATORS:
            return "invalid"
    return None


def _edition_error(mti: str, spec: Spec) -> str | None:
    if len(mti) == 4 and mti.isascii() and mti.isdigit() and mti[0] != EDITIONS[spec.edition]:
        return f"MTI {mti!r}: version digit must be {EDITIONS[spec.edition]} for ISO 8583:{spec.edition}"
    return None


def _peek_mti(hex_message: str, spec: Spec) -> str | None:
    try:
        r = _Reader(bytes.fromhex("".join(hex_message.split())))
        if spec.mti_encoding == "bcd":
            return _read_digits(r, 4, "MTI")
        return r.take(4, "MTI").decode("ascii", errors="replace")
    except (ValueError, DecodeError):
        return None


def validate(hex_message: str, spec: Spec) -> list[str]:
    mti = _peek_mti(hex_message, spec)
    wrong_edition = _edition_error(mti, spec) if mti else None
    if wrong_edition:
        return [wrong_edition]
    try:
        message = decode(hex_message, spec)
    except DecodeError as e:
        return [str(e)]
    errors = []
    mti = message["mti"]
    if len(mti) != 4 or not all(c in _DIGITS for c in mti):
        errors.append(f"MTI {mti!r}: must be 4 digits")
    for num, value in message["fields"].items():
        f = spec.fields[num]
        label = f"field {num} ({f.name})"
        size = len(value)
        if f.type == "b":
            size //= 2
            if len(value) % 2:
                errors.append(f"{label}: binary value must be even-length hex")
        if size > f.max:
            errors.append(f"{label}: length {size} exceeds max {f.max}")
        problem = _bad_char(f.type, value)
        if problem:
            # never quote the value of a PAN or track field
            c = next(c for c in value if _bad_char(f.type, c))
            shown = "" if f.sensitive else f" {c!r}"
            errors.append(f"{label}: {problem} character{shown} in {f.type} field")
    return errors
