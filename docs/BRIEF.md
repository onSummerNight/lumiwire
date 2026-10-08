# Brief: Step 7b — binary type `b` and `llllvar`

**Goal:** the spec format supports type `"b"` (raw bytes) and length `"llllvar"` (4-digit prefix), end to end in decode, encode and validate.

**Why now:** User chose "format features first" (no public 2003 field tables). Both are edition-independent and publicly documented; see `docs/ISO2003-GAPS.md`.

## Steps
1. `spec.py`: add `"b"` to TYPES and `"llllvar"` to LENGTHS. For `b`, `max` counts bytes.
2. `decode.py`/`encode.py`: `b` values are raw bytes in the message and an uppercase hex string in the result/JSON (2 hex chars per byte); the length prefix counts bytes and uses the field's `encoding` like other prefixes. `llllvar` = 4-digit prefix, same rules as ll/lllvar.
3. `validate.py`: `b` value must be even-length hex within `max` bytes.
4. Tests: a test spec `tests/spec_binary.json` (edition 1987) with field 52 `b` fixed 8 and field 55 `b` llllvar max 999; one synthetic message using both; round-trip both ways; odd-length hex → `EncodeError`; existing tests unchanged.
5. Small commit: `feat: binary field type and llllvar length`.

## Acceptance check
`.venv/bin/pytest -q`: all pass (46 existing + new binary/llllvar tests).

## Constraints
- Don't change behaviour for existing types/lengths or masking. Standard library only, synthetic data only.
- Update the spec-format section of README for the new values (docs only, no new examples).

## Out of scope
Tertiary bitmap, subfields, field renumbering, other type letters, the 2003 spec file.

## Result
Done. `.venv/bin/pytest -q` → 54 passed (46 existing + 8 new in tests/test_binary.py). Code commit: feat: binary field type and llllvar length.
Manager: for type `b` the spec `encoding` applies to the length prefix only (noted in README). Validate's odd-length check can't trigger on decoded messages (decode always yields even hex); it is there per the brief. Docs commit is local, not pushed.
