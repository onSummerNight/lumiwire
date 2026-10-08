"""Load and check a JSON field spec."""
import json
from dataclasses import dataclass
from pathlib import Path

TYPES = {"n", "an", "ans", "z", "b"}  # b: raw bytes, shown as hex; max counts bytes
PREFIX_WIDTH = {"llvar": 2, "lllvar": 3, "llllvar": 4}
LENGTHS = {"fixed", *PREFIX_WIDTH}
ENCODINGS = {"ascii", "bcd"}
SENSITIVE = {"pan", "track"}
EDITIONS = {"1987": "0", "2003": "2"}  # edition -> MTI version digit


class SpecError(ValueError):
    pass


@dataclass(frozen=True)
class Field:
    number: int
    name: str
    type: str
    length: str
    max: int
    encoding: str
    sensitive: str | None = None


@dataclass(frozen=True)
class Spec:
    name: str
    edition: str
    mti_encoding: str
    bitmap_encoding: str
    fields: dict[int, Field]


def _check(value, allowed, what):
    if value not in allowed:
        raise SpecError(f"{what}: {value!r} not one of {sorted(allowed)}")
    return value


def load_spec(path: str | Path) -> Spec:
    try:
        raw = json.loads(Path(path).read_text())
    except json.JSONDecodeError as e:
        raise SpecError(f"{path}: invalid JSON: {e}") from e
    fields = {}
    for key, f in raw.get("fields", {}).items():
        num = int(key)
        if not 2 <= num <= 128:
            raise SpecError(f"field {key}: number must be 2..128")
        if not isinstance(f.get("max"), int) or f["max"] < 1:
            raise SpecError(f"field {key}: max must be a positive integer")
        sens = f.get("sensitive")
        if sens is not None:
            _check(sens, SENSITIVE, f"field {key} sensitive")
        fields[num] = Field(
            number=num,
            name=f["name"],
            type=_check(f.get("type"), TYPES, f"field {key} type"),
            length=_check(f.get("length"), LENGTHS, f"field {key} length"),
            max=f["max"],
            encoding=_check(f.get("encoding"), ENCODINGS, f"field {key} encoding"),
            sensitive=sens,
        )
    if not fields:
        raise SpecError("spec has no fields")
    return Spec(
        name=raw["name"],
        edition=_check(raw.get("edition"), EDITIONS, "edition"),
        mti_encoding=_check(raw.get("mti_encoding"), ENCODINGS, "mti_encoding"),
        bitmap_encoding=_check(raw.get("bitmap_encoding"), {"hex", "binary"}, "bitmap_encoding"),
        fields=fields,
    )
