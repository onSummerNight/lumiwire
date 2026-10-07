# Brief: Step 3 — encode from JSON + round-trip

**Goal:** `encode(message, spec) -> str` in `src/lumiwire/encode.py` builds the hex message from `{"mti": "0200", "fields": {"2": "...", ...}}`, and `lumiwire encode FILE.json` prints it.

**Why now:** Top of Next. Round-trip is a v1 success check, and validate (Later) depends on both directions.

## Steps
1. `encode()`: MTI, bitmap(s) and fields, mirroring `decode()` exactly: raw-byte bitmaps, set bit 1 and add the secondary bitmap only when a field > 64 is present; llvar/lllvar prefixes count digits/chars; BCD left-padded to a whole byte. Accept field keys as int or str.
2. Raise `EncodeError` (field number + reason) for: field not in spec, value longer than `max`, fixed field with the wrong length, non-digit in an `n` field.
3. `tests/test_encode.py`: for every synthetic message in `tests/messages.py`, `encode(decode(hex)) == hex` (case-insensitive) and `decode(encode(obj)) == obj`; one test per `EncodeError` case.
4. CLI `encode`: read the JSON file, `--spec` defaults to the bundled spec like `decode`, print uppercase hex; `EncodeError`/`SpecError`/bad JSON → stderr, exit 1. Update the CLI stub test (no stub left except `validate`).

## Acceptance check
`.venv/bin/pytest -q` — all pass (13 existing + new encode tests), including round-trip on both synthetic messages.

## Constraints
- Don't change `decode()`, `mask()` or bitmap handling (DECISIONS 2026-10-07). Encode never masks; it takes real (synthetic) values.
- Standard library only. Synthetic data only. Small commit: `feat: encode from JSON with round-trip tests`.

## Out of scope
Validate command, `bitmap_encoding` handling, JSON output from `decode`, type checks for an/ans/z beyond length.

## Result
Done. `.venv/bin/pytest -q` -> `22 passed in 0.03s` (13 existing + 9 new: round-trip x2, string keys, 4 EncodeError cases, 2 CLI).
Manager to decide: a `bcd` field with non-`n` type still rejects non-digits (needed to pack BCD); empty value in an `n` field is rejected as non-digit.
