import json
from importlib import resources

import pytest
from typer.testing import CliRunner

from lumiwire.cli import app
from lumiwire.spec import SpecError, load_spec

DEMO = resources.files("lumiwire") / "specs" / "iso8583_1987.json"


def test_demo_spec_loads():
    spec = load_spec(DEMO)
    assert {2, 3, 4, 11, 35, 39, 41, 70} == set(spec.fields)
    assert spec.fields[2].sensitive == "pan"
    assert spec.fields[35].sensitive == "track"


def test_bad_spec_rejected(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"name": "x", "mti_encoding": "ascii", "bitmap_encoding": "hex",
                             "fields": {"2": {"name": "a", "type": "q", "length": "fixed", "max": 1, "encoding": "ascii"}}}))
    with pytest.raises(SpecError, match="type"):
        load_spec(p)


def test_cli_stub_runs():
    r = CliRunner().invoke(app, ["validate", "00"])
    assert r.exit_code == 2
