# Brief: Step 4a — honour `bitmap_encoding`

**Goal:** decode and encode read/write bitmaps per spec: `"binary"` = 8 raw bytes per bitmap, `"hex"` = 16 ASCII hex chars per bitmap.

**Why now:** Next says resolve `bitmap_encoding` before validate; user chose "honour both" (DECISIONS 2026-10-07).

## Steps
1. Demo spec `iso8583_1987.json`: set `"bitmap_encoding": "binary"` (current behaviour, so existing messages stay valid).
2. `decode.py`: bitmap reader takes the spec's encoding; for `"hex"` read 16 ASCII chars, check they are hex digits (else `DecodeError` with offset), convert to bits. Secondary bitmap the same way.
3. `encode.py`: mirror it; for `"hex"` emit the bitmap as uppercase ASCII hex chars.
4. Tests: a second spec fixture `tests/spec_hex_bitmap.json` (copy of demo, `"hex"`), one synthetic message using it with a secondary bitmap; round-trip both ways; non-hex char in an ASCII bitmap raises `DecodeError`.

## Acceptance check
`.venv/bin/pytest -q` — all pass (22 existing + new bitmap tests).

## Constraints
- Don't change field parsing, masking or CLI behaviour. Existing tests must pass unchanged.
- Synthetic data only. Small commit: `feat: honour spec bitmap_encoding`.

## Out of scope
Validate command and broken-message tests (next brief, 4b), any other spec keys.
