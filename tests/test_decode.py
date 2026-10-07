from importlib import resources

import pytest

from lumiwire.decode import DecodeError, decode
from lumiwire.spec import load_spec
from messages import DECODED_0200, DECODED_0800, MSG_0200, MSG_0800

SPEC = load_spec(resources.files("lumiwire") / "specs" / "iso8583_1987.json")


def test_decode_0200():
    assert decode(MSG_0200, SPEC) == DECODED_0200


def test_decode_0800_secondary_bitmap():
    assert decode(MSG_0800, SPEC) == DECODED_0800


def test_truncated_raises():
    with pytest.raises(DecodeError, match="field 41"):
        decode(MSG_0200[:-4], SPEC)


def test_trailing_data_raises():
    with pytest.raises(DecodeError, match="trailing"):
        decode(MSG_0800 + "00", SPEC)


def test_unknown_field_raises():
    # bit 5 set in the primary bitmap, no spec entry
    with pytest.raises(DecodeError, match="field 5"):
        decode("30323030" + "08" + "00" * 7, SPEC)
