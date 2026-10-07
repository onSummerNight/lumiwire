"""Encode a message dict into a hex string; mirrors decode()."""
from .spec import Spec


class EncodeError(ValueError):
    pass


def _digits(value: str) -> bytes:
    """BCD digits, left-padded to a whole byte."""
    if len(value) % 2:
        value = "0" + value
    return bytes.fromhex(value)


def encode(message: dict, spec: Spec) -> str:
    mti = str(message.get("mti", ""))
    if len(mti) != 4 or not mti.isdigit():
        raise EncodeError(f"MTI: must be 4 digits, got {mti!r}")
    try:
        fields = {int(k): v for k, v in message.get("fields", {}).items()}
    except ValueError as e:
        raise EncodeError(f"field key: {e}") from e
    out = _digits(mti) if spec.mti_encoding == "bcd" else mti.encode("ascii")

    bitmap = bytearray(16 if any(n > 64 for n in fields) else 8)
    if len(bitmap) == 16:
        bitmap[0] |= 0x80
    body = b""
    for num in sorted(fields):
        f = spec.fields.get(num)
        if f is None:
            raise EncodeError(f"field {num}: no entry in spec")
        value = fields[num]
        if not isinstance(value, str):
            raise EncodeError(f"field {num}: value must be a string")
        if len(value) > f.max:
            raise EncodeError(f"field {num}: length {len(value)} exceeds max {f.max}")
        if f.length == "fixed" and len(value) != f.max:
            raise EncodeError(f"field {num}: fixed length {f.max}, got {len(value)}")
        if (f.type == "n" or f.encoding == "bcd") and not value.isdigit() and value:
            raise EncodeError(f"field {num}: non-digit in numeric value")
        bitmap[(num - 1) // 8] |= 0x80 >> (num - 1) % 8
        if f.length != "fixed":
            width = 2 if f.length == "llvar" else 3
            prefix = str(len(value)).zfill(width)
            body += _digits(prefix) if f.encoding == "bcd" else prefix.encode("ascii")
        try:
            body += _digits(value) if f.encoding == "bcd" else value.encode("ascii")
        except UnicodeEncodeError:
            raise EncodeError(f"field {num}: non-ASCII character") from None
    if spec.bitmap_encoding == "hex":
        bitmap = bitmap.hex().upper().encode("ascii")
    return (out + bytes(bitmap) + body).hex().upper()
