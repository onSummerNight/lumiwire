import re
from importlib import resources

from typer.testing import CliRunner

from lumiwire.cli import app
from lumiwire.decode import decode
from lumiwire.mask import mask
from lumiwire.spec import load_spec
from messages import MSG_0200, MSG_0800

SPEC = load_spec(resources.files("lumiwire") / "specs" / "iso8583_1987.json")
PAN = "4111111111111111"


def test_mask_hides_pan_and_track():
    masked = mask(decode(MSG_0200, SPEC), SPEC)
    assert masked["fields"][2] == "411111******1111"
    assert PAN not in str(masked)
    assert not re.search(r"\d{13,}", masked["fields"][35])
    assert masked["fields"][3] == "000000"


def test_mask_leaves_input_and_other_message_alone():
    result = decode(MSG_0200, SPEC)
    mask(result, SPEC)
    assert result["fields"][2] == PAN
    assert mask(decode(MSG_0800, SPEC), SPEC) == decode(MSG_0800, SPEC)


def test_cli_masks_by_default():
    r = CliRunner().invoke(app, ["decode", MSG_0200])
    assert r.exit_code == 0
    assert "MTI 0200" in r.output
    assert "002 Primary account number: 411111******1111" in r.output
    assert PAN not in r.output


def test_cli_unmask_shows_full():
    r = CliRunner().invoke(app, ["decode", MSG_0200, "--unmask"])
    assert r.exit_code == 0
    assert PAN in r.output
    assert "4111111111111111=25121010000" in r.output


def test_cli_truncated_exits_1():
    r = CliRunner().invoke(app, ["decode", MSG_0200[:-4]])
    assert r.exit_code == 1
    assert "error" in r.output
