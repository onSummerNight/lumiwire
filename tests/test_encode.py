import json

import pytest
from typer.testing import CliRunner

from lumiwire.cli import DEFAULT_SPEC, app
from lumiwire.decode import decode
from lumiwire.encode import EncodeError, encode
from lumiwire.spec import load_spec

from messages import DECODED_0200, DECODED_0800, MSG_0200, MSG_0800

SPEC = load_spec(DEFAULT_SPEC)
CASES = [(MSG_0200, DECODED_0200), (MSG_0800, DECODED_0800)]


@pytest.mark.parametrize("hex_msg,obj", CASES)
def test_round_trip(hex_msg, obj):
    assert encode(decode(hex_msg, SPEC), SPEC).lower() == hex_msg.lower()
    assert decode(encode(obj, SPEC), SPEC) == obj


def test_string_keys():
    obj = {"mti": "0800", "fields": {"11": "000001", "70": "001"}}
    assert encode(obj, SPEC).lower() == MSG_0800.lower()


@pytest.mark.parametrize("fields,text", [
    ({99: "1"}, "field 99"),
    ({2: "1" * 20}, "exceeds max"),
    ({3: "00000"}, "fixed length"),
    ({3: "00000A"}, "non-digit"),
])
def test_encode_errors(fields, text):
    with pytest.raises(EncodeError, match=text):
        encode({"mti": "0200", "fields": fields}, SPEC)


def test_cli_encode(tmp_path):
    f = tmp_path / "m.json"
    f.write_text(json.dumps({"mti": "0800", "fields": {"11": "000001", "70": "001"}}))
    r = CliRunner().invoke(app, ["encode", str(f)])
    assert r.exit_code == 0
    assert r.output.strip() == MSG_0800.upper()


def test_cli_encode_errors(tmp_path):
    bad = tmp_path / "bad.json"
    bad.write_text("{nope")
    assert CliRunner().invoke(app, ["encode", str(bad)]).exit_code == 1
    bad.write_text(json.dumps({"mti": "0200", "fields": {"99": "1"}}))
    assert CliRunner().invoke(app, ["encode", str(bad)]).exit_code == 1
