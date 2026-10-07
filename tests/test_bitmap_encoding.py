from pathlib import Path

import pytest

from lumiwire.decode import DecodeError, decode
from lumiwire.encode import encode
from lumiwire.spec import load_spec

from messages import DECODED_0800

SPEC = load_spec(Path(__file__).parent / "spec_hex_bitmap.json")

# MSG_0800 with both bitmaps as 16 ASCII hex chars each
MSG_0800_HEX = "".join([
    "30383030",
    "38303230303030303030303030303030",   # "8020000000000000"
    "30343030303030303030303030303030",   # "0400000000000000"
    "000001",
    "0001",
])


def test_hex_bitmap_round_trip():
    assert decode(MSG_0800_HEX, SPEC) == DECODED_0800
    assert encode(DECODED_0800, SPEC) == MSG_0800_HEX.upper()


def test_non_hex_bitmap_char():
    bad = MSG_0800_HEX.replace("38303230", "3830325a", 1)  # "802Z..."
    with pytest.raises(DecodeError, match="non-hex"):
        decode(bad, SPEC)
