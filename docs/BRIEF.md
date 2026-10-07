# Brief: Step 4b — validate command

**Goal:** `validate(hex_message, spec) -> list[str]` in `src/lumiwire/validate.py` returns every problem found (empty list = valid), and `lumiwire validate HEX` reports them.

**Why now:** Top of Next and the last v1 success check: "validate rejects deliberately broken synthetic messages with a clear error".

## Steps
1. Structure: run `decode()`; a `DecodeError` becomes the single error (structure broken, nothing further to check). MTI must be 4 digits with a valid 1987 version digit `0`.
2. Content, per field: `n` digits only; `an` letters/digits; `ans` printable ASCII; `z` digits plus `=` or `D` separator; length within `max`. Each error names field number and spec name, e.g. `field 3 (Processing code): non-digit 'A'`. Collect all, don't stop at the first.
3. Error text must never contain an unmasked PAN or track value (mask before quoting a value, or don't quote it for sensitive fields).
4. `tests/test_validate.py`: both good synthetic messages → `[]`; a set of at least 6 broken messages built in `tests/messages.py` (truncated, unknown field bit, bad MTI, non-digit in `n`, bad char in `an`, bad track separator) → one expected error each; no error string contains the full test PAN.
5. CLI `validate`: `--spec` defaults to the bundled spec; prints `OK` and exits 0, or one error per line on stderr and exits 1. Replace the remaining stub test.

## Acceptance check
`.venv/bin/pytest -q` — all pass (24 existing + new validate tests).

## Constraints
- Don't change `decode()`, `encode()` or `mask()` behaviour; reuse them. Standard library only, synthetic data only.
- Small commit: `feat: validate command with broken-message tests`.

## Out of scope
Field-level semantics (dates, amounts, processing-code tables), MAC/PIN checks, JSON output.

## Result
Done. `.venv/bin/pytest -q` -> `43 passed in 0.04s` (24 existing + 19 new/changed).
- validate() reuses decode(); structure error is the single result, else MTI + per-field content errors, all collected.
- PAN/track errors never quote the value; tested.
- Removed the now-unused `_todo` helper in cli.py.
- Decision for manager: `max` length check is mostly redundant (decode already enforces it); kept as a cheap guard.
