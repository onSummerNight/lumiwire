"""Mask sensitive fields in a decoded result."""
from .spec import Spec


def _star_pan(pan: str) -> str:
    if len(pan) < 13:
        return "*" * len(pan)
    return pan[:6] + "*" * (len(pan) - 10) + pan[-4:]


def _mask_track(track: str) -> str:
    n = 0
    while n < len(track) and track[n].isdigit():
        n += 1
    return _star_pan(track[:n]) + "*" * (len(track) - n)


def mask(result: dict, spec: Spec) -> dict:
    fields = dict(result["fields"])
    for num, value in fields.items():
        kind = spec.fields[num].sensitive
        if kind == "pan":
            fields[num] = _star_pan(value)
        elif kind == "track":
            fields[num] = _mask_track(value)
    return {**result, "fields": fields}
