import re
from importlib import resources

import pytest
from typer.testing import CliRunner

from lumiwire.cli import app
from lumiwire.decode import decode
from lumiwire.encode import encode
from lumiwire.mask import mask
from lumiwire.spec import load_spec
from lumiwire.validate import validate
from messages import DECODED_2100, DECODED_2800, MSG_0200, MSG_2100, MSG_2800

SPECS = resources.files("lumiwire") / "specs"
SPEC = load_spec(SPECS / "iso8583_2003.json")
SPEC_1987 = load_spec(SPECS / "iso8583_1987.json")
PAN = "4111111111111111"
CASES = [(MSG_2100, DECODED_2100), (MSG_2800, DECODED_2800)]


def test_edition():
    assert SPEC.edition == "2003"


@pytest.mark.parametrize("hex_msg,obj", CASES)
def test_round_trip(hex_msg, obj):
    assert decode(hex_msg, SPEC) == obj
    assert encode(obj, SPEC).lower() == hex_msg.lower()
    assert encode(decode(hex_msg, SPEC), SPEC).lower() == hex_msg.lower()


@pytest.mark.parametrize("hex_msg,obj", CASES)
def test_validate_ok(hex_msg, obj):
    assert validate(hex_msg, SPEC) == []


def test_masked_has_no_full_pan_or_track():
    masked = mask(decode(MSG_2100, SPEC), SPEC)
    assert PAN not in str(masked)
    assert not re.search(r"\d{13,}", masked["fields"][35])
    r = CliRunner().invoke(app, ["decode", MSG_2100, "--spec", str(SPECS / "iso8583_2003.json")])
    assert r.exit_code == 0
    assert PAN not in r.output and "4111111111111111=" not in r.output


def test_1987_spec_flags_version_digit():
    errors = validate(MSG_2800, SPEC_1987)
    assert any("version digit must be 0 for ISO 8583:1987" in e for e in errors)


def test_1987_spec_rejects_2100():
    # edition is checked before decoding, so the real cause is the only error
    errors = validate(MSG_2100, SPEC_1987)
    assert len(errors) == 1
    assert "version digit must be 0 for ISO 8583:1987" in errors[0]


def test_1987_spec_rejects_2800_with_one_error():
    errors = validate(MSG_2800, SPEC_1987)
    assert len(errors) == 1
    assert "version digit must be 0 for ISO 8583:1987" in errors[0]


def test_2003_spec_rejects_1987_message():
    errors = validate(MSG_0200, SPEC)
    assert len(errors) == 1
    assert "version digit must be 2 for ISO 8583:2003" in errors[0]
