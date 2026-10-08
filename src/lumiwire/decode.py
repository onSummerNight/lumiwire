"""Decode a hex-encoded ISO 8583:1987 message using a field spec."""
from .spec import PREFIX_WIDTH, Spec


class DecodeError(ValueError):
    pass


class _Reader:
    def __init__(self, data: bytes):
        self.data = data
        self.pos = 0

    def take(self, n: int, what: str) -> bytes:
        if self.pos + n > len(self.data):
            raise DecodeError(f"{what}: need {n} bytes at offset {self.pos}, "
                              f"only {len(self.data) - self.pos} left")
        chunk = self.data[self.pos:self.pos + n]
        self.pos += n
        return chunk


def _read_digits(r: _Reader, count: int, what: str) -> str:
    """Read `count` BCD digits (left-padded to a whole byte)."""
    digits = r.take((count + 1) // 2, what).hex()
    if not digits.isdigit():
        raise DecodeError(f"{what}: non-digit in BCD at offset {r.pos}")
    return digits[len(digits) - count:]


def _read_len(r: _Reader, width: int, encoding: str, what: str) -> int:
    if encoding == "bcd":
        return int(_read_digits(r, width, what))
    text = r.take(width, what).decode("ascii", errors="replace")
    if not text.isdigit():
        raise DecodeError(f"{what}: bad length prefix {text!r} at offset {r.pos - width}")
    return int(text)


def _take_bitmap(r: _Reader, encoding: str, what: str) -> bytes:
    if encoding == "binary":
        return r.take(8, what)
    start = r.pos
    text = r.take(16, what).decode("ascii", errors="replace")
    if not all(c in "0123456789abcdefABCDEF" for c in text):
        raise DecodeError(f"{what}: non-hex character in {text!r} at offset {start}")
    return bytes.fromhex(text)


def _read_bitmap(r: _Reader, encoding: str) -> list[int]:
    bits = _take_bitmap(r, encoding, "primary bitmap")
    if bits[0] & 0x80:
        bits += _take_bitmap(r, encoding, "secondary bitmap")
    return [i + 1 for i in range(len(bits) * 8)
            if bits[i // 8] & (0x80 >> i % 8) and i != 0]


def decode(hex_message: str, spec: Spec) -> dict:
    try:
        r = _Reader(bytes.fromhex("".join(hex_message.split())))
    except ValueError as e:
        raise DecodeError(f"invalid hex: {e}") from e
    if spec.mti_encoding == "bcd":
        mti = _read_digits(r, 4, "MTI")
    else:
        mti = r.take(4, "MTI").decode("ascii", errors="replace")
    present = _read_bitmap(r, spec.bitmap_encoding)
    fields = {}
    for num in present:
        f = spec.fields.get(num)
        if f is None:
            raise DecodeError(f"field {num}: no entry in spec (offset {r.pos})")
        what = f"field {num}"
        start = r.pos
        if f.length == "fixed":
            n = f.max
        else:
            n = _read_len(r, PREFIX_WIDTH[f.length], f.encoding, what)
            if n > f.max:
                raise DecodeError(f"{what}: length {n} exceeds max {f.max} at offset {start}")
        if f.type == "b":
            fields[num] = r.take(n, what).hex().upper()
        elif f.encoding == "bcd":
            fields[num] = _read_digits(r, n, what)
        else:
            fields[num] = r.take(n, what).decode("ascii", errors="replace")
    if r.pos != len(r.data):
        raise DecodeError(f"{len(r.data) - r.pos} trailing bytes after last field at offset {r.pos}")
    return {"mti": mti, "fields": fields}
