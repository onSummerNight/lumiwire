from importlib import resources

import pytest

from lumiwire.spec import load_spec
from lumiwire.validate import validate
from messages import BROKEN, MSG_0200, MSG_0800

SPEC = load_spec(resources.files("lumiwire") / "specs" / "iso8583_1987.json")
PAN = "4111111111111111"


@pytest.mark.parametrize("msg", [MSG_0200, MSG_0800])
def test_good_messages_valid(msg):
    assert validate(msg, SPEC) == []


@pytest.mark.parametrize("name", BROKEN)
def test_broken_messages_rejected(name):
    msg, expected = BROKEN[name]
    errors = validate(msg, SPEC)
    assert len(errors) == 1, errors
    assert expected in errors[0]


@pytest.mark.parametrize("name", BROKEN)
def test_errors_never_contain_pan(name):
    assert all(PAN not in e for e in validate(BROKEN[name][0], SPEC))


def test_pan_error_does_not_quote_value():
    # F2 "4111111111111111" -> "41111111111111A1"
    msg = MSG_0200.replace("34313131313131313131313131313131", "34313131313131313131313131313141", 1)
    errors = validate(msg, SPEC)
    assert errors == ["field 2 (Primary account number): non-digit character in n field"]


def test_collects_all_errors():
    msg = BROKEN["bad_mti_nondigit"][0].replace("31313131303030303030303030", "31313131303041303030303030", 1)
    assert len(validate(msg, SPEC)) == 2


def test_mti_2100_rejected_by_1987_spec():
    from messages import MSG_0200
    msg = MSG_0200.replace("30323030", "32313030", 1)  # MTI "0200" -> "2100"
    errors = validate(msg, SPEC)
    assert any("version digit must be 0 for ISO 8583:1987" in e for e in errors)
