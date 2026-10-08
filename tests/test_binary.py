from pathlib import Path

import pytest

from lumiwire.decode import decode
from lumiwire.encode import EncodeError, encode
from lumiwire.spec import load_spec
from lumiwire.validate import validate

SPEC = load_spec(Path(__file__).parent / "spec_binary.json")

MSG = "".join([
    "30323030",              # MTI "0200"
    "0000000000001200",      # bitmap: bits 52, 55
    "0123456789ABCDEF",      # F52 fixed, 8 raw bytes
    "30303034", "DEADBEEF",  # F55 llllvar ASCII: len "0004", 4 raw bytes
])
DECODED = {"mti": "0200", "fields": {52: "0123456789ABCDEF", 55: "DEADBEEF"}}


def test_decode():
    assert decode(MSG, SPEC) == DECODED


def test_encode_and_round_trip():
    assert encode(DECODED, SPEC) == MSG
    assert encode(decode(MSG, SPEC), SPEC) == MSG


def test_lowercase_hex_encodes_same_bytes():
    obj = {"mti": "0200", "fields": {52: "0123456789abcdef", 55: "deadbeef"}}
    assert encode(obj, SPEC) == MSG


@pytest.mark.parametrize("fields,text", [
    ({55: "ABC"}, "even-length hex"),
    ({55: "ZZ"}, "even-length hex"),
    ({52: "0123"}, "fixed length 8"),
    ({55: "00" * 1000}, "exceeds max"),
])
def test_encode_rejects(fields, text):
    with pytest.raises(EncodeError, match=text):
        encode({"mti": "0200", "fields": fields}, SPEC)


def test_validate_ok():
    assert validate(MSG, SPEC) == []
